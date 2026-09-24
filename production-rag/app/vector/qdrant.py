import uuid

from qdrant_client import QdrantClient
from qdrant_client.http import models

from app.ingestion.models import Chunk

CHUNK_POINT_ID_NAMESPACE = uuid.UUID("6ba7b810-9dad-11d1-80b4-00c04fd430c8")


def build_qdrant_client(url: str, api_key: str | None = None) -> QdrantClient:
    """Create a Qdrant client from connection settings."""
    kwargs: dict[str, object] = {"url": url, "check_compatibility": False}
    if api_key:
        kwargs["api_key"] = api_key
    return QdrantClient(**kwargs)


def ensure_collection(
    client: QdrantClient,
    collection_name: str,
    vector_size: int,
) -> bool:
    """Create the collection when it does not exist. Returns True if created."""
    if client.collection_exists(collection_name):
        return False

    client.create_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(
            size=vector_size,
            distance=models.Distance.COSINE,
        ),
    )
    return True


def build_chunk_point_id(chunk: Chunk) -> str:
    """Build a deterministic point ID for stable re-indexing."""
    key = "|".join(
        [
            chunk.filename,
            str(chunk.page),
            str(chunk.row),
            chunk.sheet or "",
            str(chunk.chunk_index),
        ]
    )
    return str(uuid.uuid5(CHUNK_POINT_ID_NAMESPACE, key))


def upsert_chunk_embeddings(
    client: QdrantClient,
    collection_name: str,
    chunks: list[Chunk],
    embeddings: list[list[float]],
) -> int:
    """Upsert chunk vectors into Qdrant. Returns the number of points written."""
    if len(chunks) != len(embeddings):
        raise ValueError("chunks and embeddings must have the same length")

    if not chunks:
        return 0

    points = [
        models.PointStruct(
            id=build_chunk_point_id(chunk),
            vector=embedding,
            payload={"text": chunk.text},
        )
        for chunk, embedding in zip(chunks, embeddings, strict=True)
    ]
    client.upsert(collection_name=collection_name, points=points)
    return len(points)
