
import uuid
from typing import Protocol, List, Dict, Any, Optional

# Import the new repository and existing legacy tools tools
from .repository_pgvector import PgvectorMemoryRepository

# Import legacy internals for wrapping
# Note: We use local imports inside methods to avoid circular dependency with tools module.
# (tools -> factory -> store -> tools)


class MemoryStore(Protocol):
    """
    Interface for memory operations, abstracting the backend (Pgvector vs FAISS/SQLite).
    """
    def write_memory(
        self,
        user_id: uuid.UUID,
        type: str,
        text: str,
        metadata: Dict[str, Any],
        session_id: Optional[uuid.UUID] = None
    ) -> uuid.UUID:
        ...

    def search_memory(
        self,
        user_id: uuid.UUID,
        query_text: str,
        top_k: int = 5,
        types: Optional[List[str]] = None,
        metadata_filter: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        ...

    def get_recent_episodic(
        self, 
        user_id: uuid.UUID, 
        limit: int = 10,
        session_id: Optional[uuid.UUID] = None
    ) -> List[Dict[str, Any]]:
        ...
        
    def ingest_document(self, file_path: str, user_id: uuid.UUID) -> None:
        """
        Ingest a document file.
        Additional method required to bridge the gap with rag_tools.update_vector_store.
        """
        ...

class PgvectorMemoryStore:
    """
    Implementation using Postgres + pgvector.
    """
    def __init__(self, repository: PgvectorMemoryRepository):
        self.repository = repository

    def write_memory(
        self,
        user_id: uuid.UUID,
        type: str,
        text: str,
        metadata: Dict[str, Any],
        session_id: Optional[uuid.UUID] = None
    ) -> uuid.UUID:
        return self.repository.write_memory(user_id, type, text, metadata, session_id)

    def search_memory(
        self,
        user_id: uuid.UUID,
        query_text: str,
        top_k: int = 5,
        types: Optional[List[str]] = None,
        metadata_filter: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        return self.repository.search_memory(user_id, query_text, top_k, types, metadata_filter)

    def get_recent_episodic(
        self,
        user_id: uuid.UUID,
        limit: int = 10,
        session_id: Optional[uuid.UUID] = None
    ) -> List[Dict[str, Any]]:
        return self.repository.get_recent_episodic(user_id, limit, session_id)

    def ingest_document(self, file_path: str, user_id: uuid.UUID) -> None:
        """
        Parses document and writes chunks to memory repository as 'semantic' memories.
        """
        # Reusing the loading logic from rag_tools would be ideal to avoid code duplication.
        # However, rag_tools is coupled to FAISS.
        # We'll pull the loading logic here or refactor rag_tools to allow splitting loader from store.
        # For this step, we'll duplicate the loader logic to ensure isolation or importing if possible.
        from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        from pathlib import Path
        
        loader = PyPDFLoader(file_path) if file_path.endswith(".pdf") else Docx2txtLoader(file_path)
        documents = loader.load()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        docs = text_splitter.split_documents(documents)
        
        filename = Path(file_path).name
        
        for doc in docs:
            metadata = {
                "source": file_path,
                "file_name": filename,
                "chunk_index": doc.metadata.get("start_index", 0) # approximation if available
            }
            # We treat document chunks as 'semantic' memory
            self.write_memory(
                user_id=user_id,
                type="semantic",
                text=doc.page_content,
                metadata=metadata
            )


class FaissMemoryStore:
    """
    Legacy implementation wrapping existing tools logic.
    """
    def write_memory(
        self,
        user_id: uuid.UUID,
        type: str,
        text: str,
        metadata: Dict[str, Any],
        session_id: Optional[uuid.UUID] = None
    ) -> uuid.UUID:
        # Route based on type
        if type == "semantic":
            # Adapting:
            # If metadata has 'key', use _remember_fact?
            key = metadata.get("key")
            if key:
                from ..tools.memory_tools import _remember_fact
                _remember_fact(key, text, user_id=str(user_id))
                return uuid.uuid4() # Mock ID
            
            # Fallback: if we can't map to legacy, we might log warning or do nothing.
            print(f"[FaissStore] Warning: Cannot fully map write_memory type={type} to legacy tools.")
            return uuid.uuid4()

        else:
             # Default to UserFact if we can derive a key?
             pass
        return uuid.uuid4()

    def search_memory(
        self,
        user_id: uuid.UUID,
        query_text: str,
        top_k: int = 5,
        types: Optional[List[str]] = None,
        metadata_filter: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        # Map to _query_uploaded_documents (FAISS) 
        
        results = []
        
        from langchain_community.vectorstores import FAISS
        from ..tools.rag_tools import FAISS_INDEX_PATH, embeddings
        import os
        
        if os.path.exists(FAISS_INDEX_PATH) and os.listdir(FAISS_INDEX_PATH):
             try:
                db = FAISS.load_local(FAISS_INDEX_PATH, embeddings, allow_dangerous_deserialization=True)
                # Note: Legacy ignores user_id.
                docs = db.similarity_search(query_text, k=top_k)
                for doc in docs:
                    results.append({
                        "id": uuid.uuid4(),
                        "text": doc.page_content,
                        "type": "semantic",
                        "metadata": doc.metadata,
                        "score": 0.0 
                    })
             except Exception as e:
                 print(f"[FaissStore] Error: {e}")
        
        return results

    def get_recent_episodic(self, user_id: uuid.UUID, limit: int = 10, session_id: Optional[uuid.UUID] = None) -> List[Dict[str, Any]]:
        return []

    def ingest_document(self, file_path: str, user_id: uuid.UUID) -> None:
        from ..tools.rag_tools import update_vector_store as _legacy_update_vector_store
        # Delegate to legacy function
        _legacy_update_vector_store(file_path)
