
from functools import lru_cache
from ..config import settings
from .store import MemoryStore, PgvectorMemoryStore, FaissMemoryStore
from .repository_pgvector import PgvectorMemoryRepository
from .embeddings import EmbeddingService

@lru_cache()
def get_embedding_service() -> EmbeddingService:
    return EmbeddingService()

def get_memory_store() -> MemoryStore:
    """
    Factory function to return the configured MemoryStore implementation.
    """
    backend = settings.MEMORY_BACKEND.lower()
    
    if backend == "pgvector":
        embedding_service = get_embedding_service()
        repository = PgvectorMemoryRepository(embedding_service)
        return PgvectorMemoryStore(repository)
    
    elif backend == "faiss":
        return FaissMemoryStore()
    
    else:
        raise ValueError(f"Invalid MEMORY_BACKEND: {backend}. Must be 'pgvector' or 'faiss'.")
