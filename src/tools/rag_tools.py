"""
RAG (Retrieval Augmented Generation) tools for document querying
"""



# Refactor: Use SafeTool and local schemas
from .base import SafeTool, RiskLevel
from .schemas.rag_schemas import QueryUploadedDocumentsSchema

from ..memory.factory import get_memory_store
from ..utils.context import get_user_id
import uuid

def update_vector_store(file_path: str) -> None:
    """Loads, splits, and indexes a single document file with metadata."""
    try:
        # For simplicity in this migration, we assume current user.
        # In a real async upload, user_id should be passed.
        # But 'update_vector_store' signature in prompt 4B/4E wasn't explicitly changed.
        # We get user_id from context or default to a system user?
        # rag_tools usage context: likely called during upload API which has user context.
        user_id = get_user_id()
        if not user_id:
            # Fallback or error? Existing logic didn't use user_id.
            # We generate a dummy or raise error?
            # Existing logic was Multi-Tenant Unsafe.
            # We must use user_id now.
             raise ValueError("User context required for uploading documents.")
             
        store = get_memory_store()
        store.ingest_document(file_path, uuid.UUID(str(user_id)))
        
    except Exception as e:
        print(f"Error updating vector store: {e}")
        raise e

def _query_uploaded_documents(query: str) -> str:
    user_id = get_user_id()
    if not user_id:
        # If context missing, we can't query securely.
        return "Error: User context required to query documents."

    store = get_memory_store()
    try:
        results = store.search_memory(
            user_id=uuid.UUID(str(user_id)),
            query_text=query,
            top_k=3,
            types=["semantic"] # Assuming documents are semantic
        )
        
        if not results:
             return "No relevant information found in documents."
             
        context_parts = []
        for doc in results:
            # Format matches old output for consistency
            # Old: "--- (Source: {source}) ---\n{content}"
            meta = doc.get("metadata", {})
            source = meta.get("file_name", "Unknown Source")
            content = doc.get("text", "")
            context_parts.append(f"--- (Source: {source}) ---\n{content}")
            
        context = "\n\n".join(context_parts)
        return f"Relevant information from documents:\n{context}"
        
    except Exception as e:
        return f"Error querying documents: {e}"

# --- Tool Construction ---

query_uploaded_documents = SafeTool.from_func(
    func=_query_uploaded_documents,
    name="query_uploaded_documents",
    description="Queries the content of all previously uploaded documents.",
    args_schema=QueryUploadedDocumentsSchema,
    risk_level=RiskLevel.MEDIUM
)
