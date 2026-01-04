from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from ..database import get_db
from ..auth.dependencies import get_current_user
from ..models import User, Memory
from ..schemas.memory import MemoryCreate, MemoryRead, MemorySearch, MemoryUpdate
from ..memory.write import write_memory, compute_content_hash
from ..memory.retrieve import retrieve_memories
from ..memory.embeddings import embeddings
from ..utils.redaction import redact_text

router = APIRouter(prefix="/memories", tags=["Memory"])

@router.get("/", response_model=List[MemoryRead])
def list_memories(
    type: Optional[str] = None,
    q: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    stmt = db.query(Memory).filter(
        Memory.user_id == user.id,
        Memory.is_deleted == False
    )
    
    if type:
        stmt = stmt.filter(Memory.type == type)
        
    if q:
        # Basic text match or semantic? Prompt A2.5 implies filters. "q" implies search?
        # A2.5 #1 says "Query params: type, q, limit". Usually q=text match.
        # But for vector store, simple text match might be ilike.
        stmt = stmt.filter(Memory.content.ilike(f"%{q}%"))
        
    results = stmt.order_by(Memory.created_at.desc()).offset(offset).limit(limit).all()
    return results

@router.post("/", response_model=MemoryRead)
def create_memory(
    item: MemoryCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    mem_id = write_memory(
        db=db,
        user_id=user.id,
        session_id=None, # User created context
        type_=item.type,
        source="user",
        content=item.content,
        metadata=item.metadata
    )
    
    return db.query(Memory).filter(Memory.id == mem_id).first()

@router.post("/search", response_model=List[MemoryRead])
def search_memories(
    params: MemorySearch,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    results = retrieve_memories(
        db=db,
        user_id=str(user.id),
        query_text=params.query,
        types=params.types,
        top_k=params.top_k,
        min_score=params.min_score
    )
    return results

@router.delete("/{memory_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_memory(
    memory_id: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    mem = db.query(Memory).filter(Memory.id == memory_id, Memory.user_id == user.id).first()
    if not mem:
        raise HTTPException(status_code=404, detail="Memory not found")
        
    mem.is_deleted = True
    db.commit()
    return 

@router.patch("/{memory_id}", response_model=MemoryRead)
def update_memory(
    memory_id: str,
    update: MemoryUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    mem = db.query(Memory).filter(Memory.id == memory_id, Memory.user_id == user.id, Memory.is_deleted == False).first()
    if not mem:
        raise HTTPException(status_code=404, detail="Memory not found")
        
    if update.content:
        safe_content = redact_text(update.content)
        mem.content = safe_content
        mem.content_hash = compute_content_hash(safe_content)
        # Re-embed
        vectors = embeddings.embed_texts([safe_content])
        mem.embedding = vectors[0]
        
    if update.metadata:
        # Merge or replace? Prompt says "update content (re-embed), update metadata".
        # Assuming replace based on typical PUT, but key-based merge for PATCH is friendlier.
        # I'll do a simple merge on top of existing
        current = dict(mem.metadata_)
        current.update(update.metadata)
        mem.metadata_ = current
        
    db.commit()
    db.refresh(mem)
    return mem
