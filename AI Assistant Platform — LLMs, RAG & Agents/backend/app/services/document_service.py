import io
import time
from typing import List
from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.models import Document, DocumentChunk, DocumentStatus
from app.services.rag_service import generate_embedding
from app.core.config import settings


# ─── Text Extraction ─────────────────────────────────────────────────────────

def extract_text_from_pdf(file_bytes: bytes) -> str:
    import pdfplumber
    text_parts = []
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                text_parts.append(t)
    return "\n\n".join(text_parts)


def extract_text_from_docx(file_bytes: bytes) -> str:
    from docx import Document as DocxDocument
    doc = DocxDocument(io.BytesIO(file_bytes))
    return "\n".join(p.text for p in doc.paragraphs if p.text.strip())


def extract_text_from_xlsx(file_bytes: bytes) -> str:
    import openpyxl
    wb = openpyxl.load_workbook(io.BytesIO(file_bytes), data_only=True)
    rows = []
    for sheet in wb.worksheets:
        rows.append(f"[Sheet: {sheet.title}]")
        for row in sheet.iter_rows(values_only=True):
            clean = [str(c) for c in row if c is not None]
            if clean:
                rows.append("\t".join(clean))
    return "\n".join(rows)


def extract_text(file_bytes: bytes, file_type: str) -> str:
    extractors = {
        "pdf": extract_text_from_pdf,
        "docx": extract_text_from_docx,
        "xlsx": extract_text_from_xlsx,
        "txt": lambda b: b.decode("utf-8", errors="ignore"),
        "md": lambda b: b.decode("utf-8", errors="ignore"),
    }
    fn = extractors.get(file_type.lower())
    if not fn:
        raise ValueError(f"Unsupported file type: {file_type}")
    return fn(file_bytes)


# ─── Chunking ─────────────────────────────────────────────────────────────────

def chunk_text(text: str, chunk_size: int = None, overlap: int = None) -> List[str]:
    """
    Recursive character-based chunking.
    Splits on paragraphs first, then sentences, then characters.
    """
    size = chunk_size or settings.CHUNK_SIZE
    ovlp = overlap or settings.CHUNK_OVERLAP

    if len(text) <= size:
        return [text]

    chunks = []
    start = 0
    while start < len(text):
        end = min(start + size, len(text))

        # Try to split on paragraph boundary
        if end < len(text):
            para_break = text.rfind("\n\n", start, end)
            if para_break > start + size // 2:
                end = para_break
            else:
                sent_break = text.rfind(". ", start, end)
                if sent_break > start + size // 2:
                    end = sent_break + 1

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        start = end - ovlp

    return chunks


def estimate_tokens(text: str) -> int:
    """Rough approximation: ~4 chars per token for Portuguese."""
    return len(text) // 4


# ─── Full Pipeline ─────────────────────────────────────────────────────────────

async def process_document(
    document_id: str,
    file_bytes: bytes,
    file_type: str,
    db: AsyncSession,
) -> dict:
    """
    Full indexing pipeline:
    1. Update status → processing
    2. Extract text
    3. Chunk
    4. Generate embeddings (batch)
    5. Upsert to pgvector
    6. Update document metadata
    """
    t0 = time.time()

    # Mark as processing
    doc = await db.get(Document, document_id)
    doc.status = DocumentStatus.PROCESSING
    await db.commit()

    try:
        # 1. Extract
        raw_text = extract_text(file_bytes, file_type)

        # 2. Chunk
        chunks = chunk_text(raw_text)

        # 3. Embed + persist
        total_tokens = 0
        for i, chunk_content in enumerate(chunks):
            embedding = await generate_embedding(chunk_content)
            tokens = estimate_tokens(chunk_content)
            total_tokens += tokens

            chunk = DocumentChunk(
                document_id=document_id,
                chunk_index=i,
                content=chunk_content,
                embedding=embedding,
                tokens=tokens,
            )
            db.add(chunk)

        # 4. Update document
        doc.status = DocumentStatus.INDEXED
        doc.chunks_count = len(chunks)
        doc.tokens_count = total_tokens
        await db.commit()

        return {
            "document_id": document_id,
            "chunks": len(chunks),
            "tokens": total_tokens,
            "elapsed": round(time.time() - t0, 2),
        }

    except Exception as e:
        doc.status = DocumentStatus.ERROR
        await db.commit()
        raise e
