"""
RAG (Retrieval Augmented Generation) tools for document querying
"""



# Refactor: Use SafeTool and local schemas
from .base import SafeTool, RiskLevel
from .schemas.rag_schemas import QueryUploadedDocumentsSchema

from ..database import SessionLocal
from ..memory.write import write_memory
from ..memory.retrieve import retrieve_memories
import uuid
import os

def update_vector_store(file_path: str) -> None:
    """Loads, splits, and indexes a single document file with metadata."""
    try:
        user_id = get_user_id()
        if not user_id:
             raise ValueError("User context required for uploading documents.")
             
        # Simple ingestion: Read whole file and store as one memory (or simple chunks)
        # For now, simplistic approach.
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
            
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
            
        # Basic Chunking? Max specific to provider? 
        # Embeddings provider handles truncation/redaction.
        # We store as type="DOCUMENT" (semantic).
        
        db = SessionLocal()
        try:
            write_memory(
                db=db,
                user_id=str(user_id),
                session_id=None,
                type_="DOCUMENT",
                source="upload",
                content=text, # Provider will redact/embed. If too long, it might truncate.
                metadata={"file_name": os.path.basename(file_path)}
            )
            # Todo: Better chunking strategy
        finally:
            db.close()
        
    except Exception as e:
        print(f"Error updating vector store: {e}")
        raise e

def _query_uploaded_documents(query: str) -> str:
    user_id = get_user_id()
    if not user_id:
        return "Error: User context required to query documents."

    db = SessionLocal()
    try:
        results = retrieve_memories(
            db=db,
            user_id=str(user_id),
            query_text=query,
            types=["DOCUMENT"],
            top_k=3,
            min_score=0.65
        )
        
        if not results:
             return "No relevant information found in documents."
             
        context_parts = []
        for mem in results:
            meta = mem.metadata_ or {}
            source = meta.get("file_name", "Unknown Source")
            content = mem.content
            context_parts.append(f"--- (Source: {source}) ---\n{content}")
            
        context = "\n\n".join(context_parts)
        return f"Relevant information from documents:\n{context}"
        
    except Exception as e:
        return f"Error querying documents: {e}"
    finally:
        db.close()


# --- Tool Construction ---

query_uploaded_documents = SafeTool.from_func(
    func=_query_uploaded_documents,
    name="query_uploaded_documents",
    description="Queries the content of all previously uploaded documents.",
    args_schema=QueryUploadedDocumentsSchema,
    risk_level=RiskLevel.MEDIUM
)
