class EmbeddingProviderError(Exception):
    """Base error for embedding provider failures."""


class EmbeddingTimeoutError(EmbeddingProviderError):
    """Raised when an embedding request exceeds the configured timeout."""


class EmbeddingServiceError(EmbeddingProviderError):
    """Raised when the external embedding service fails."""

    def __init__(self, message: str, *, status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code
