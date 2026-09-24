from abc import ABC, abstractmethod

from app.llm.models import LLMRequest, LLMResponse


class LLMProvider(ABC):
    """Abstract interface for LLM backends."""

    @abstractmethod
    async def generate(self, request: LLMRequest) -> LLMResponse:
        """Generate a completion from the given request."""
