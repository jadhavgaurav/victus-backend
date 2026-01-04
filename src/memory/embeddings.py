from typing import List
import os
from ..config import settings
from ..utils.logging import get_logger
from ..utils.redaction import redact_text

logger = get_logger(__name__)

class EmbeddingsProvider:
    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        raise NotImplementedError

class LocalEmbeddings(EmbeddingsProvider):
    """
    Deterministic fake embeddings for testing/dev.
    """
    def __init__(self, dim: int = 1536):
        self.dim = dim

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        # Deterministic pseudo-random based on text length/content
        import random
        results = []
        for text in texts:
            # Seed with hash of text to be deterministic
            random.seed(hash(text))
            # Generate normalized vector
            vec = [random.uniform(-1, 1) for _ in range(self.dim)]
            norm = sum(x*x for x in vec) ** 0.5
            vec = [x/norm for x in vec]
            results.append(vec)
        return results

class OpenAIEmbeddingsProvider(EmbeddingsProvider):
    """
    OpenAI Embeddings using text-embedding-3-small (default).
    """
    def __init__(self, dim: int = 1536):
        from openai import OpenAI
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = "text-embedding-3-small"
        self.dim = dim # 3-small supports dimensions, or we use default 1536

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        # Redact before sending to OpenAI
        safe_texts = [redact_text(t) for t in texts]
        
        # Batching could be added here if needed
        data = self.client.embeddings.create(
            input=safe_texts, 
            model=self.model,
            dimensions=self.dim
        ).data
        return [d.embedding for d in data]

def get_embeddings_provider() -> EmbeddingsProvider:
    provider_type = getattr(settings, "EMBEDDINGS_PROVIDER", "local")
    
    if provider_type == "openai":
        if not settings.OPENAI_API_KEY:
             logger.warning("OpenAI API Key missing, falling back to local embeddings.")
             return LocalEmbeddings()
        return OpenAIEmbeddingsProvider()
    else:
        return LocalEmbeddings()

# Global instance
embeddings = get_embeddings_provider()
