"""Index documents from a directory into the local Qdrant collection."""

import argparse
import asyncio
import sys
from pathlib import Path

from app.embeddings import OpenAIEmbeddingProvider
from app.indexing import index_documents
from app.settings import Settings
from app.vector import build_qdrant_client


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Index documents into Qdrant")
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=Path("data/sample"),
        help="Directory containing documents to index",
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=None,
        help="Override chunk size from settings",
    )
    parser.add_argument(
        "--chunk-overlap",
        type=int,
        default=None,
        help="Override chunk overlap from settings",
    )
    return parser.parse_args()


def main() -> None:
    settings = Settings()
    if not settings.openai_api_key:
        print("OPENAI_API_KEY is not configured", file=sys.stderr)
        raise SystemExit(1)

    args = _parse_args()
    chunk_size = args.chunk_size if args.chunk_size is not None else settings.chunk_size
    chunk_overlap = (
        args.chunk_overlap if args.chunk_overlap is not None else settings.chunk_overlap
    )

    embedding_provider = OpenAIEmbeddingProvider(
        api_key=settings.openai_api_key,
        default_model=settings.openai_embedding_model,
        timeout_seconds=settings.embedding_timeout_seconds,
    )
    qdrant_client = build_qdrant_client(
        url=settings.qdrant_url,
        api_key=settings.qdrant_api_key,
    )

    result = asyncio.run(
        index_documents(
            input_dir=args.input_dir,
            embedding_provider=embedding_provider,
            qdrant_client=qdrant_client,
            collection_name=settings.qdrant_collection_name,
            vector_size=settings.qdrant_vector_size,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            embedding_batch_size=settings.embedding_batch_size,
        )
    )

    print(f"Files processed: {result.files_processed}")
    print(f"Chunks indexed: {result.chunks_indexed}")
    if result.skipped_files:
        print(f"Skipped files: {', '.join(result.skipped_files)}")


if __name__ == "__main__":
    main()
