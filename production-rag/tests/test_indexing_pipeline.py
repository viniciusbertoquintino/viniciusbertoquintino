import asyncio
from pathlib import Path
from unittest.mock import MagicMock

from fpdf import FPDF

from app.embeddings import EmbeddingProvider, EmbeddingRequest, EmbeddingResponse
from app.indexing import index_documents


class FixedSizeEmbeddingProvider(EmbeddingProvider):
    def __init__(self, vector_size: int) -> None:
        self._vector_size = vector_size

    async def embed(self, request: EmbeddingRequest) -> EmbeddingResponse:
        embeddings = [
            [float(dimension) for dimension in range(self._vector_size)]
            for _ in request.texts
        ]
        return EmbeddingResponse(embeddings=embeddings, model="fake-embedding")


def _create_pdf(path: Path, text: str) -> None:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)
    pdf.multi_cell(0, 10, text)
    pdf.output(str(path))


def test_index_documents_embeds_and_upserts_chunks(tmp_path: Path) -> None:
    _create_pdf(tmp_path / "policy.pdf", "Index this policy text for retrieval.")

    qdrant_client = MagicMock()
    qdrant_client.collection_exists.return_value = True

    result = asyncio.run(
        index_documents(
        input_dir=tmp_path,
        embedding_provider=FixedSizeEmbeddingProvider(vector_size=4),
        qdrant_client=qdrant_client,
        collection_name="production_rag_chunks",
        vector_size=4,
        chunk_size=20,
        chunk_overlap=5,
        embedding_batch_size=8,
        )
    )

    assert result.files_processed == 1
    assert result.chunks_indexed >= 1
    qdrant_client.upsert.assert_called_once()
    points = qdrant_client.upsert.call_args.kwargs["points"]
    assert len(points) == result.chunks_indexed
    assert "Index this policy" in points[0].payload["text"]


def test_index_documents_runs_via_asyncio(tmp_path: Path) -> None:
    _create_pdf(tmp_path / "policy.pdf", "Short text")

    qdrant_client = MagicMock()
    qdrant_client.collection_exists.return_value = False

    result = asyncio.run(
        index_documents(
            input_dir=tmp_path,
            embedding_provider=FixedSizeEmbeddingProvider(vector_size=3),
            qdrant_client=qdrant_client,
            collection_name="production_rag_chunks",
            vector_size=3,
            chunk_size=100,
            chunk_overlap=10,
            embedding_batch_size=16,
        )
    )

    assert result.chunks_indexed == 1
    qdrant_client.create_collection.assert_called_once()
