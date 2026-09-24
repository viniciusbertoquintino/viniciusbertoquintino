class LLMProviderError(Exception):
    """Base error for LLM provider failures."""


class LLMTimeoutError(LLMProviderError):
    """Raised when an LLM request exceeds the configured timeout."""


class LLMServiceError(LLMProviderError):
    """Raised when the external LLM service fails."""

    def __init__(self, message: str, *, status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code
