import asyncio

import pytest

from app.embeddings import EmbeddingProvider, EmbeddingRequest, EmbeddingResponse


class FakeEmbeddingProvider(EmbeddingProvider):
    async def embed(self, request: EmbeddingRequest) -> EmbeddingResponse:
        model = request.model or "fake-embedding"
        embeddings = [
            [float(index), float(len(text)), float(len(text) * 2)]
            for index, text in enumerate(request.texts)
        ]
        return EmbeddingResponse(
            embeddings=embeddings,
            model=model,
            usage_tokens=sum(len(text) for text in request.texts),
        )


def test_embedding_provider_cannot_be_instantiated_directly() -> None:
    with pytest.raises(TypeError):
        EmbeddingProvider()  # type: ignore[abstract]


def test_concrete_provider_implements_embed() -> None:
    provider = FakeEmbeddingProvider()
    response = asyncio.run(
        provider.embed(
            EmbeddingRequest(texts=["hello", "world"], model="test-embedding")
        )
    )

    assert response.model == "test-embedding"
    assert len(response.embeddings) == 2
    assert response.embeddings[0] == [0.0, 5.0, 10.0]
    assert response.embeddings[1] == [1.0, 5.0, 10.0]
    assert response.usage_tokens == 10
