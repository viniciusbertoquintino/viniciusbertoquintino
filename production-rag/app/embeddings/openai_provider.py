import asyncio

from openai import APIConnectionError, APIStatusError, APITimeoutError, AsyncOpenAI, RateLimitError

from app.embeddings.errors import EmbeddingServiceError, EmbeddingTimeoutError
from app.embeddings.models import EmbeddingRequest, EmbeddingResponse
from app.embeddings.provider import EmbeddingProvider


class OpenAIEmbeddingProvider(EmbeddingProvider):
    """OpenAI embeddings adapter."""

    def __init__(
        self,
        *,
        api_key: str,
        default_model: str = "text-embedding-3-small",
        timeout_seconds: float = 30.0,
        client: AsyncOpenAI | None = None,
    ) -> None:
        self._default_model = default_model
        self._timeout_seconds = timeout_seconds
        self._client = client or AsyncOpenAI(api_key=api_key)

    async def embed(self, request: EmbeddingRequest) -> EmbeddingResponse:
        model = request.model or self._default_model

        try:
            response = await asyncio.wait_for(
                self._client.embeddings.create(
                    model=model,
                    input=request.texts,
                ),
                timeout=self._timeout_seconds,
            )
        except TimeoutError as exc:
            raise EmbeddingTimeoutError("Embedding request timed out") from exc
        except APITimeoutError as exc:
            raise EmbeddingTimeoutError("Embedding request timed out") from exc
        except RateLimitError as exc:
            raise EmbeddingServiceError("Embedding rate limit exceeded", status_code=429) from exc
        except APIStatusError as exc:
            raise EmbeddingServiceError(
                "Embedding service returned an error",
                status_code=exc.status_code,
            ) from exc
        except APIConnectionError as exc:
            raise EmbeddingServiceError("Failed to connect to embedding service") from exc

        usage = response.usage
        embeddings = [list(item.embedding) for item in response.data]

        return EmbeddingResponse(
            embeddings=embeddings,
            model=response.model,
            usage_tokens=usage.total_tokens if usage else None,
        )
