from app.ingestion.models import Chunk, Document


class TextChunker:
    """Split document text into overlapping character-based chunks."""

    def __init__(self, chunk_size: int = 1000, overlap: int = 200) -> None:
        if chunk_size < 1:
            raise ValueError(f"chunk_size must be at least 1, got: {chunk_size}")
        if overlap < 0:
            raise ValueError(f"overlap must be non-negative, got: {overlap}")
        if overlap >= chunk_size:
            raise ValueError(
                f"overlap must be smaller than chunk_size ({chunk_size}), got: {overlap}"
            )

        self._chunk_size = chunk_size
        self._overlap = overlap

    def chunk(self, document: Document) -> list[Chunk]:
        text = document.text.strip()
        if not text:
            return []

        if len(text) <= self._chunk_size:
            return [self._build_chunk(document=document, text=text, chunk_index=0)]

        chunks: list[Chunk] = []
        stride = self._chunk_size - self._overlap
        start = 0
        chunk_index = 0

        while start < len(text):
            end = start + self._chunk_size
            chunks.append(
                self._build_chunk(
                    document=document,
                    text=text[start:end],
                    chunk_index=chunk_index,
                )
            )
            chunk_index += 1
            if end >= len(text):
                break
            start += stride

        return chunks

    def chunk_many(self, documents: list[Document]) -> list[Chunk]:
        chunks: list[Chunk] = []
        for document in documents:
            chunks.extend(self.chunk(document))
        return chunks

    def _build_chunk(self, document: Document, text: str, chunk_index: int) -> Chunk:
        return Chunk(
            text=text,
            chunk_index=chunk_index,
            filename=document.filename,
            source_type=document.source_type,
            page=document.page,
            row=document.row,
            sheet=document.sheet,
            title=document.title,
            author=document.author,
            created_at=document.created_at,
            modified_at=document.modified_at,
        )
