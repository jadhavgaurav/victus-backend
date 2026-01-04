"""
Document upload and management endpoints
"""

import os
import shutil
from typing import Optional
from datetime import datetime
from fastapi import APIRouter, Request, UploadFile, File, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User
from ..tools import update_vector_store
from ..config import settings
FAISS_INDEX_PATH = settings.FAISS_INDEX_PATH
from ..utils.logging import get_logger
from ..auth.dependencies import get_optional_user, get_current_user
from .schemas import DocumentsResponse, DocumentItem, DocumentStatusResponse
from ..models.file import FileMetadata
from ..models.user import User # Ensure User is imported for type hint if needed
from ..security.audit import log_security_event, SecurityEventType

logger = get_logger(__name__)
router = APIRouter(prefix="/api", tags=["Documents"])


@router.post("/upload")
async def upload_document(
    request: Request,
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    current_user = Depends(get_optional_user), # Temporarily keep optional, but enforce check
    db: Session = Depends(get_db)
):
    """Upload a document for RAG processing."""
    if not current_user:
        raise HTTPException(status_code=401, detail="Authentication required for upload")

    from ..security.files import validate_and_save_upload
    from ..models.file import FileMetadata
    
    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)
    
    try:
        stored_name, original_name, size = validate_and_save_upload(file, upload_dir)
        
        # Determine MIME
        ext = os.path.splitext(stored_name)[1]
        mime = "application/pdf" if ext == ".pdf" else "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        if ext == ".txt": mime = "text/plain"
        if ext == ".md": mime = "text/markdown"
        
        # Create DB Record
        db_file = FileMetadata(
            user_id=current_user.id,
            original_name=original_name,
            stored_name=stored_name,
            mime_type=mime,
            size_bytes=size
        )
        db.add(db_file)
        db.commit()
        
        # Process RAG
        full_path = os.path.join(upload_dir, stored_name)
        background_tasks.add_task(update_vector_store, full_path)
        
        log_security_event(
            SecurityEventType.FILE_UPLOAD, 
            user_id=str(current_user.id), 
            details={"filename": original_name, "size": size, "mime": mime},
            ip_address=request.client.host if request.client else None
        )
        logger.info(f"File uploaded safely: {original_name} -> {stored_name}")
        
        return {
            "status": "success",
            "filename": original_name,
            "id": str(db_file.id),
            "detail": "File received and is being processed."
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error uploading file: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error uploading file"
        )


@router.get("/documents", response_model=DocumentsResponse)
async def get_documents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get list of all uploaded documents for the current user.
    """
    try:
        files = db.query(FileMetadata).filter(FileMetadata.user_id == current_user.id).all()
        
        doc_items = []
        total_size = 0
        
        # We need to check if indexed.
        # This is tricky because FAISS index doesn't link back to DB IDs easily unless we store ID in metadata.
        # MVP: check if file status is "ready"?
        # For now assume ready if in DB, or we can check file existence.
        # Ideally we should have a `status` column in FileMetadata.
        
        for f in files:
            total_size += f.size_bytes
            doc_items.append(DocumentItem(
                filename=f.original_name,
                size=f.size_bytes,
                upload_date=f.created_at.isoformat(),
                status="ready", # Simplified
                indexed=True
            ))
            
        doc_items.sort(key=lambda x: x.upload_date, reverse=True)
            
        return DocumentsResponse(
            documents=doc_items,
            total=len(doc_items),
            total_size=total_size
        )

    except Exception as e:
        logger.error(f"Error getting documents: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving documents"
        )


@router.delete("/documents/{filename}")
async def delete_document(
    filename: str,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a document.
    """
    try:
        # Find file in DB
        db_file = db.query(FileMetadata).filter(
            FileMetadata.user_id == current_user.id,
            FileMetadata.original_name == filename # Assuming simple mapping for now
        ).first()
        
        if not db_file:
             raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found"
            )
            
        # Delete from disk
        upload_dir = "uploads"
        file_path = os.path.join(upload_dir, db_file.stored_name)
        
        if os.path.exists(file_path):
            os.remove(file_path)
            
        # Delete from DB
        db.delete(db_file)
        db.commit()
        
        log_security_event(
            SecurityEventType.FILE_DELETE, 
            user_id=str(current_user.id), 
            details={"filename": filename, "file_id": str(db_file.id)},
            ip_address=request.client.host if request.client else None
        )
        logger.info(f"Deleted document: {filename} (ID: {db_file.id})")
        
        return {"status": "success", "filename": filename}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting document: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error deleting document"
        )


@router.get("/documents/status", response_model=DocumentStatusResponse)
async def get_document_status(
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_optional_user)
):
    """
    Get document processing status.
    """
    try:
        upload_dir = "uploads"
        if not os.path.exists(upload_dir):
            return DocumentStatusResponse(total=0, indexed=0, processing=0, failed=0)
        
        total = 0
        indexed = 0
        processing = 0
        
        for filename in os.listdir(upload_dir):
            if filename.endswith(".pdf") or filename.endswith(".docx"):
                total += 1
                # Check if indexed
                if os.path.exists(FAISS_INDEX_PATH) and os.path.isdir(FAISS_INDEX_PATH):
                    if len(os.listdir(FAISS_INDEX_PATH)) > 0:
                        indexed += 1
                    else:
                        processing += 1
                else:
                    processing += 1
        
        return DocumentStatusResponse(
            total=total,
            indexed=indexed,
            processing=processing,
            failed=0  # We don't track failures currently
        )
    except Exception as e:
        logger.error(f"Error getting document status: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving document status"
        )

