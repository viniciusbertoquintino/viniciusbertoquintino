from abc import ABC, abstractmethod

from app.embeddings.models import EmbeddingRequest, EmbeddingResponse


class EmbeddingProvider(ABC):
    """Abstract interface for embedding backends."""

    @abstractmethod
    async def embed(self, request: EmbeddingRequest) -> EmbeddingResponse:
        """Generate embeddings for the given texts."""
