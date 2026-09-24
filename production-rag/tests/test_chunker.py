import pytest

from app.ingestion import Chunk, Document, TextChunker


def _sample_document(text: str = "abcdefghij") -> Document:
    return Document(
        filename="politica-ferias.pdf",
        source_type="pdf",
        text=text,
        page=2,
    )


def test_short_text_produces_single_chunk() -> None:
    document = _sample_document(text="texto curto")
    chunks = TextChunker(chunk_size=100, overlap=10).chunk(document)

    assert len(chunks) == 1
    assert chunks[0].text == "texto curto"
    assert chunks[0].chunk_index == 0


def test_custom_chunk_size_and_overlap_change_output() -> None:
    document = _sample_document(text="abcdefghijklmnopqrstuvwxyz")

    small_chunks = TextChunker(chunk_size=10, overlap=2).chunk(document)
    large_chunks = TextChunker(chunk_size=20, overlap=5).chunk(document)

    assert len(small_chunks) > len(large_chunks)
    assert all(len(chunk.text) <= 10 for chunk in small_chunks)
    assert large_chunks[0].text == "abcdefghijklmnopqrst"


def test_chunk_preserves_source_metadata() -> None:
    document = Document(
        filename="reembolsos.csv",
        source_type="csv",
        text="linha de reembolso",
        row=3,
        title="Processo de Reembolso",
        author="Financeiro",
    )
    chunk = TextChunker(chunk_size=100, overlap=10).chunk(document)[0]

    assert isinstance(chunk, Chunk)
    assert chunk.filename == "reembolsos.csv"
    assert chunk.source_type == "csv"
    assert chunk.row == 3
    assert chunk.page is None
    assert chunk.title == "Processo de Reembolso"
    assert chunk.author == "Financeiro"


def test_chunk_many_processes_multiple_documents() -> None:
    documents = [
        _sample_document(text="abc"),
        Document(
            filename="sla.xlsx",
            source_type="xlsx",
            text="defghi",
            sheet="Prioridades",
            row=1,
        ),
    ]
    chunks = TextChunker(chunk_size=3, overlap=1).chunk_many(documents)

    assert len(chunks) == 4
    assert chunks[0].filename == "politica-ferias.pdf"
    assert chunks[-1].sheet == "Prioridades"


def test_rejects_overlap_greater_than_or_equal_to_chunk_size() -> None:
    with pytest.raises(ValueError, match="overlap must be smaller than chunk_size"):
        TextChunker(chunk_size=10, overlap=10)

    with pytest.raises(ValueError, match="overlap must be smaller than chunk_size"):
        TextChunker(chunk_size=10, overlap=15)


def test_empty_text_returns_no_chunks() -> None:
    chunks = TextChunker(chunk_size=10, overlap=2).chunk(_sample_document(text=""))

    assert chunks == []


def test_whitespace_only_text_returns_no_chunks() -> None:
    chunks = TextChunker(chunk_size=10, overlap=2).chunk(_sample_document(text="   \n\t  "))

    assert chunks == []


def test_text_equal_to_chunk_size_produces_single_chunk() -> None:
    text = "abcde"
    chunks = TextChunker(chunk_size=5, overlap=2).chunk(_sample_document(text=text))

    assert len(chunks) == 1
    assert chunks[0].text == text
    assert chunks[0].chunk_index == 0


def test_last_chunk_can_be_smaller_than_chunk_size() -> None:
    chunks = TextChunker(chunk_size=5, overlap=2).chunk(_sample_document(text="abcdefghi"))

    assert len(chunks) == 3
    assert chunks[-1].text == "ghi"
    assert len(chunks[-1].text) < 5


def test_chunk_indices_are_sequential() -> None:
    chunks = TextChunker(chunk_size=4, overlap=1).chunk(_sample_document(text="abcdefghij"))

    assert [chunk.chunk_index for chunk in chunks] == [0, 1, 2]


def test_consecutive_chunks_share_overlap() -> None:
    chunks = TextChunker(chunk_size=5, overlap=2).chunk(_sample_document(text="abcdefghij"))

    assert chunks[0].text[-2:] == chunks[1].text[:2]
    assert chunks[1].text[-2:] == chunks[2].text[:2]


def test_rejects_invalid_chunk_size() -> None:
    with pytest.raises(ValueError, match="chunk_size must be at least 1"):
        TextChunker(chunk_size=0, overlap=0)

    with pytest.raises(ValueError, match="chunk_size must be at least 1"):
        TextChunker(chunk_size=-1, overlap=0)


def test_rejects_negative_overlap() -> None:
    with pytest.raises(ValueError, match="overlap must be non-negative"):
        TextChunker(chunk_size=10, overlap=-1)


def test_chunk_many_with_empty_list_returns_empty() -> None:
    chunks = TextChunker(chunk_size=5, overlap=1).chunk_many([])

    assert chunks == []


def test_chunk_many_skips_empty_documents() -> None:
    documents = [
        _sample_document(text=""),
        _sample_document(text="   "),
        Document(
            filename="sla.xlsx",
            source_type="xlsx",
            text="abc",
            sheet="Prioridades",
            row=1,
        ),
    ]
    chunks = TextChunker(chunk_size=3, overlap=0).chunk_many(documents)

    assert len(chunks) == 1
    assert chunks[0].text == "abc"
    assert chunks[0].filename == "sla.xlsx"


def test_strips_leading_and_trailing_whitespace_before_chunking() -> None:
    chunks = TextChunker(chunk_size=3, overlap=0).chunk(_sample_document(text="  abc  "))

    assert len(chunks) == 1
    assert chunks[0].text == "abc"
