import asyncio
from unittest.mock import AsyncMock, MagicMock

import pytest
from openai import APIConnectionError, APIStatusError, RateLimitError

from app.llm import LLMMessage, LLMRequest
from app.llm.errors import LLMServiceError, LLMTimeoutError
from app.llm.openai_provider import OpenAIProvider


async def _slow_completion(**kwargs: object) -> MagicMock:
    await asyncio.sleep(1)
    return MagicMock()


def test_openai_provider_raises_timeout_error() -> None:
    mock_client = MagicMock()
    mock_client.chat.completions.create = _slow_completion

    provider = OpenAIProvider(
        api_key="test-key",
        client=mock_client,
        timeout_seconds=0.01,
    )

    with pytest.raises(LLMTimeoutError, match="timed out"):
        asyncio.run(
            provider.generate(
                LLMRequest(messages=[LLMMessage(role="user", content="Hi")])
            )
        )


def test_openai_provider_maps_rate_limit_error() -> None:
    mock_client = MagicMock()
    mock_client.chat.completions.create = AsyncMock(
        side_effect=RateLimitError(
            "rate limit exceeded",
            response=MagicMock(status_code=429),
            body=None,
        )
    )

    provider = OpenAIProvider(api_key="test-key", client=mock_client)

    with pytest.raises(LLMServiceError, match="rate limit") as exc_info:
        asyncio.run(
            provider.generate(
                LLMRequest(messages=[LLMMessage(role="user", content="Hi")])
            )
        )

    assert exc_info.value.status_code == 429


def test_openai_provider_maps_connection_error() -> None:
    mock_client = MagicMock()
    mock_client.chat.completions.create = AsyncMock(
        side_effect=APIConnectionError(request=MagicMock())
    )

    provider = OpenAIProvider(api_key="test-key", client=mock_client)

    with pytest.raises(LLMServiceError, match="Failed to connect"):
        asyncio.run(
            provider.generate(
                LLMRequest(messages=[LLMMessage(role="user", content="Hi")])
            )
        )


def test_openai_provider_maps_api_status_error() -> None:
    mock_client = MagicMock()
    mock_client.chat.completions.create = AsyncMock(
        side_effect=APIStatusError(
            "service unavailable",
            response=MagicMock(status_code=503),
            body=None,
        )
    )

    provider = OpenAIProvider(api_key="test-key", client=mock_client)

    with pytest.raises(LLMServiceError, match="returned an error") as exc_info:
        asyncio.run(
            provider.generate(
                LLMRequest(messages=[LLMMessage(role="user", content="Hi")])
            )
        )

    assert exc_info.value.status_code == 503
