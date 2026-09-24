from unittest.mock import MagicMock

import pytest
from qdrant_client import QdrantClient
from qdrant_client.http import models

from app.settings import Settings
from app.vector.qdrant import build_qdrant_client, ensure_collection


def test_settings_define_qdrant_collection_defaults() -> None:
    settings = Settings(_env_file=None)

    assert settings.qdrant_collection_name == "production_rag_chunks"
    assert settings.qdrant_vector_size == 1536


def test_build_qdrant_client_returns_qdrant_client() -> None:
    client = build_qdrant_client(url="http://localhost:6333")

    assert isinstance(client, QdrantClient)


def test_ensure_collection_creates_when_missing() -> None:
    client = MagicMock()
    client.collection_exists.return_value = False

    created = ensure_collection(
        client=client,
        collection_name="production_rag_chunks",
        vector_size=1536,
    )

    assert created is True
    client.create_collection.assert_called_once_with(
        collection_name="production_rag_chunks",
        vectors_config=models.VectorParams(
            size=1536,
            distance=models.Distance.COSINE,
        ),
    )


def test_ensure_collection_is_idempotent_when_exists() -> None:
    client = MagicMock()
    client.collection_exists.return_value = True

    created = ensure_collection(
        client=client,
        collection_name="production_rag_chunks",
        vector_size=1536,
    )

    assert created is False
    client.create_collection.assert_not_called()


@pytest.mark.integration
def test_create_collection_against_local_qdrant() -> None:
    settings = Settings(_env_file=None)
    client = build_qdrant_client(
        url=settings.qdrant_url,
        api_key=settings.qdrant_api_key,
    )

    try:
        created = ensure_collection(
            client=client,
            collection_name=settings.qdrant_collection_name,
            vector_size=settings.qdrant_vector_size,
        )
    except Exception as exc:  # noqa: BLE001
        pytest.skip(f"Local Qdrant is not available: {exc}")

    assert client.collection_exists(settings.qdrant_collection_name)
    if created:
        client.delete_collection(settings.qdrant_collection_name)
