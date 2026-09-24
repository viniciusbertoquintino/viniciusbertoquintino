import asyncio

from openai import APIConnectionError, APIStatusError, APITimeoutError, AsyncOpenAI, RateLimitError

from app.llm.errors import LLMServiceError, LLMTimeoutError
from app.llm.models import LLMRequest, LLMResponse
from app.llm.provider import LLMProvider


class OpenAIProvider(LLMProvider):
    """OpenAI chat completions adapter."""

    def __init__(
        self,
        *,
        api_key: str,
        default_model: str = "gpt-4o-mini",
        timeout_seconds: float = 30.0,
        client: AsyncOpenAI | None = None,
    ) -> None:
        self._default_model = default_model
        self._timeout_seconds = timeout_seconds
        self._client = client or AsyncOpenAI(api_key=api_key)

    async def generate(self, request: LLMRequest) -> LLMResponse:
        model = request.model or self._default_model
        payload: dict[str, object] = {
            "model": model,
            "messages": [
                {"role": message.role, "content": message.content}
                for message in request.messages
            ],
        }
        if request.temperature is not None:
            payload["temperature"] = request.temperature

        try:
            response = await asyncio.wait_for(
                self._client.chat.completions.create(**payload),
                timeout=self._timeout_seconds,
            )
        except TimeoutError as exc:
            raise LLMTimeoutError("LLM request timed out") from exc
        except APITimeoutError as exc:
            raise LLMTimeoutError("LLM request timed out") from exc
        except RateLimitError as exc:
            raise LLMServiceError("LLM rate limit exceeded", status_code=429) from exc
        except APIStatusError as exc:
            raise LLMServiceError(
                "LLM service returned an error",
                status_code=exc.status_code,
            ) from exc
        except APIConnectionError as exc:
            raise LLMServiceError("Failed to connect to LLM service") from exc

        choice = response.choices[0]
        usage = response.usage

        return LLMResponse(
            content=choice.message.content or "",
            model=response.model,
            prompt_tokens=usage.prompt_tokens if usage else None,
            completion_tokens=usage.completion_tokens if usage else None,
        )
