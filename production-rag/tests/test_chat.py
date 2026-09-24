from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from app.dependencies import get_llm_provider
from app.llm import LLMProvider, LLMRequest, LLMResponse
from app.llm.errors import LLMServiceError, LLMTimeoutError
from app.main import app


class FakeLLMProvider(LLMProvider):
    def __init__(self) -> None:
        self.requests: list[LLMRequest] = []

    async def generate(self, request: LLMRequest) -> LLMResponse:
        self.requests.append(request)
        return LLMResponse(
            content="test answer",
            model="fake-model",
            prompt_tokens=10,
            completion_tokens=5,
        )


@pytest.fixture
def client() -> Generator[tuple[TestClient, FakeLLMProvider], None, None]:
    fake_provider = FakeLLMProvider()
    app.dependency_overrides[get_llm_provider] = lambda: fake_provider
    with TestClient(app) as test_client:
        yield test_client, fake_provider
    app.dependency_overrides.clear()


def test_chat_returns_pydantic_response(client: tuple[TestClient, FakeLLMProvider]) -> None:
    test_client, _ = client
    response = test_client.post(
        "/chat",
        json={"messages": [{"role": "user", "content": "Hello"}]},
    )

    assert response.status_code == 200
    assert response.json() == {
        "answer": "test answer",
        "model": "fake-model",
        "prompt_tokens": 10,
        "completion_tokens": 5,
    }


def test_chat_validates_request_schema(client: tuple[TestClient, FakeLLMProvider]) -> None:
    test_client, _ = client
    response = test_client.post("/chat", json={"messages": []})

    assert response.status_code == 422


def test_chat_forwards_messages_to_provider(
    client: tuple[TestClient, FakeLLMProvider],
) -> None:
    test_client, fake_provider = client
    test_client.post(
        "/chat",
        json={
            "messages": [{"role": "user", "content": "Hello"}],
            "model": "gpt-4o-mini",
            "temperature": 0.2,
        },
    )

    assert len(fake_provider.requests) == 1
    llm_request = fake_provider.requests[0]
    assert llm_request.messages[0].content == "Hello"
    assert llm_request.model == "gpt-4o-mini"
    assert llm_request.temperature == 0.2


def test_chat_returns_504_on_provider_timeout() -> None:
    class TimeoutLLMProvider(LLMProvider):
        async def generate(self, request: LLMRequest) -> LLMResponse:
            raise LLMTimeoutError("LLM request timed out")

    app.dependency_overrides[get_llm_provider] = lambda: TimeoutLLMProvider()
    with TestClient(app) as test_client:
        response = test_client.post(
            "/chat",
            json={"messages": [{"role": "user", "content": "Hello"}]},
        )

    app.dependency_overrides.clear()
    assert response.status_code == 504
    assert response.json() == {"detail": "LLM request timed out"}


def test_chat_returns_502_on_provider_service_error() -> None:
    class FailingLLMProvider(LLMProvider):
        async def generate(self, request: LLMRequest) -> LLMResponse:
            raise LLMServiceError("LLM service returned an error", status_code=503)

    app.dependency_overrides[get_llm_provider] = lambda: FailingLLMProvider()
    with TestClient(app) as test_client:
        response = test_client.post(
            "/chat",
            json={"messages": [{"role": "user", "content": "Hello"}]},
        )

    app.dependency_overrides.clear()
    assert response.status_code == 502
    assert response.json() == {"detail": "LLM service returned an error"}


def test_chat_returns_429_on_provider_rate_limit() -> None:
    class RateLimitedLLMProvider(LLMProvider):
        async def generate(self, request: LLMRequest) -> LLMResponse:
            raise LLMServiceError("LLM rate limit exceeded", status_code=429)

    app.dependency_overrides[get_llm_provider] = lambda: RateLimitedLLMProvider()
    with TestClient(app) as test_client:
        response = test_client.post(
            "/chat",
            json={"messages": [{"role": "user", "content": "Hello"}]},
        )

    app.dependency_overrides.clear()
    assert response.status_code == 429
    assert response.json() == {"detail": "LLM rate limit exceeded"}
