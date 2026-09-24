from pathlib import Path

from qdrant_client import QdrantClient

from app.embeddings import EmbeddingProvider, EmbeddingRequest
from app.indexing.loaders import load_documents_from_directory
from app.indexing.models import IndexingResult
from app.ingestion import TextChunker
from app.vector import ensure_collection, upsert_chunk_embeddings


def _validate_embedding_dimensions(
    embeddings: list[list[float]],
    *,
    vector_size: int,
) -> None:
    for index, embedding in enumerate(embeddings):
        if len(embedding) != vector_size:
            raise ValueError(
                f"Embedding at index {index} has size {len(embedding)}, "
                f"expected {vector_size}"
            )


async def index_documents(
    *,
    input_dir: Path,
    embedding_provider: EmbeddingProvider,
    qdrant_client: QdrantClient,
    collection_name: str,
    vector_size: int,
    chunk_size: int,
    chunk_overlap: int,
    embedding_batch_size: int,
) -> IndexingResult:
    """Load documents, chunk, embed, and upsert vectors into Qdrant."""
    load_result = load_documents_from_directory(input_dir)
    chunker = TextChunker(chunk_size=chunk_size, overlap=chunk_overlap)
    chunks = chunker.chunk_many(load_result.documents)

    ensure_collection(
        client=qdrant_client,
        collection_name=collection_name,
        vector_size=vector_size,
    )

    if not chunks:
        return IndexingResult(
            files_processed=load_result.files_processed,
            chunks_indexed=0,
            skipped_files=load_result.skipped_files,
        )

    chunks_indexed = 0
    for start in range(0, len(chunks), embedding_batch_size):
        batch = chunks[start : start + embedding_batch_size]
        response = await embedding_provider.embed(
            EmbeddingRequest(texts=[chunk.text for chunk in batch])
        )
        _validate_embedding_dimensions(response.embeddings, vector_size=vector_size)
        chunks_indexed += upsert_chunk_embeddings(
            client=qdrant_client,
            collection_name=collection_name,
            chunks=batch,
            embeddings=response.embeddings,
        )

    return IndexingResult(
        files_processed=load_result.files_processed,
        chunks_indexed=chunks_indexed,
        skipped_files=load_result.skipped_files,
    )
