import asyncio
from unittest.mock import AsyncMock, MagicMock

from app.llm import LLMMessage, LLMRequest
from app.llm.openai_provider import OpenAIProvider


def test_openai_provider_returns_text_from_isolated_call() -> None:
    mock_client = MagicMock()
    mock_completion = MagicMock()
    mock_completion.choices = [MagicMock(message=MagicMock(content="Hello from OpenAI"))]
    mock_completion.model = "gpt-4o-mini"
    mock_completion.usage = MagicMock(prompt_tokens=10, completion_tokens=5)
    mock_client.chat.completions.create = AsyncMock(return_value=mock_completion)

    provider = OpenAIProvider(api_key="test-key", client=mock_client)
    response = asyncio.run(
        provider.generate(
            LLMRequest(messages=[LLMMessage(role="user", content="Say hello")])
        )
    )

    assert response.content == "Hello from OpenAI"
    assert response.model == "gpt-4o-mini"
    assert response.prompt_tokens == 10
    assert response.completion_tokens == 5
    mock_client.chat.completions.create.assert_awaited_once()
