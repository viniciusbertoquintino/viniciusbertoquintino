import asyncio

import pytest

from app.llm import LLMMessage, LLMProvider, LLMRequest, LLMResponse


class FakeLLMProvider(LLMProvider):
    async def generate(self, request: LLMRequest) -> LLMResponse:
        last_message = request.messages[-1].content
        model = request.model or "fake"
        return LLMResponse(content=f"echo:{last_message}", model=model)


def test_llm_provider_cannot_be_instantiated_directly() -> None:
    with pytest.raises(TypeError):
        LLMProvider()  # type: ignore[abstract]


def test_concrete_provider_implements_generate() -> None:
    provider = FakeLLMProvider()
    response = asyncio.run(
        provider.generate(
            LLMRequest(messages=[LLMMessage(role="user", content="hello")])
        )
    )

    assert response.content == "echo:hello"
    assert response.model == "fake"
