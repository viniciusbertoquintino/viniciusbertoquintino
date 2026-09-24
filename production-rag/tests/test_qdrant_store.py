from unittest.mock import MagicMock

import pytest

from app.ingestion.models import Chunk
from app.vector.qdrant import build_chunk_point_id, upsert_chunk_embeddings


def _sample_chunk(**overrides: object) -> Chunk:
    payload = {
        "text": "chunk text",
        "chunk_index": 0,
        "filename": "policy.pdf",
        "source_type": "pdf",
        "page": 1,
    }
    payload.update(overrides)
    return Chunk(**payload)


def test_build_chunk_point_id_is_deterministic() -> None:
    chunk = _sample_chunk()

    first = build_chunk_point_id(chunk)
    second = build_chunk_point_id(chunk)

    assert first == second


def test_build_chunk_point_id_changes_with_metadata() -> None:
    first = build_chunk_point_id(_sample_chunk(chunk_index=0))
    second = build_chunk_point_id(_sample_chunk(chunk_index=1))

    assert first != second


def test_upsert_chunk_embeddings_writes_points() -> None:
    client = MagicMock()
    chunks = [_sample_chunk(), _sample_chunk(chunk_index=1, text="other")]
    embeddings = [[0.1, 0.2], [0.3, 0.4]]

    written = upsert_chunk_embeddings(
        client=client,
        collection_name="production_rag_chunks",
        chunks=chunks,
        embeddings=embeddings,
    )

    assert written == 2
    client.upsert.assert_called_once()
    points = client.upsert.call_args.kwargs["points"]
    assert points[0].payload == {"text": "chunk text"}
    assert points[1].payload == {"text": "other"}


def test_upsert_chunk_embeddings_rejects_mismatched_lengths() -> None:
    with pytest.raises(ValueError, match="same length"):
        upsert_chunk_embeddings(
            client=MagicMock(),
            collection_name="production_rag_chunks",
            chunks=[_sample_chunk()],
            embeddings=[[0.1], [0.2]],
        )
