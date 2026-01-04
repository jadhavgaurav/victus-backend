
from typing import List
from langchain_openai import OpenAIEmbeddings
from ..config import settings

class EmbeddingService:
    """
    Wrapper around OpenAIEmbeddings to provide a stable interface
    and consistent configuration.
    """
    def __init__(self):
        self._embedder = OpenAIEmbeddings(
            model="text-embedding-3-small",
            openai_api_key=settings.OPENAI_API_KEY
        )
        self._dimension = 1536

    @property
    def dimension(self) -> int:
        return self._dimension

    def embed_text(self, text: str) -> List[float]:
        """Embed a single text string."""
        return self._embedder.embed_query(text)

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of text strings."""
        return self._embedder.embed_documents(texts)
