import asyncio
from unittest.mock import AsyncMock, MagicMock

from app.embeddings import EmbeddingRequest
from app.embeddings.openai_provider import OpenAIEmbeddingProvider


def test_openai_embedding_provider_returns_vectors_from_isolated_call() -> None:
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.data = [
        MagicMock(embedding=[0.1, 0.2, 0.3]),
        MagicMock(embedding=[0.4, 0.5, 0.6]),
    ]
    mock_response.model = "text-embedding-3-small"
    mock_response.usage = MagicMock(total_tokens=12)
    mock_client.embeddings.create = AsyncMock(return_value=mock_response)

    provider = OpenAIEmbeddingProvider(api_key="test-key", client=mock_client)
    response = asyncio.run(
        provider.embed(EmbeddingRequest(texts=["hello", "world"]))
    )

    assert response.model == "text-embedding-3-small"
    assert len(response.embeddings) == 2
    assert response.embeddings[0] == [0.1, 0.2, 0.3]
    assert response.embeddings[1] == [0.4, 0.5, 0.6]
    assert response.usage_tokens == 12
    mock_client.embeddings.create.assert_awaited_once()
