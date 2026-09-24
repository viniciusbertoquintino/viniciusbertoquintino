from pathlib import Path

SAMPLE_DOCUMENTS_DIR = Path("data/sample")
MIN_SAMPLE_DOCUMENTS = 5


def test_sample_documents_directory_exists() -> None:
    assert SAMPLE_DOCUMENTS_DIR.is_dir()


def test_sample_documents_meet_minimum_count() -> None:
    documents = [path for path in SAMPLE_DOCUMENTS_DIR.iterdir() if path.is_file()]
    assert len(documents) >= MIN_SAMPLE_DOCUMENTS


def test_sample_documents_are_non_empty() -> None:
    documents = [path for path in SAMPLE_DOCUMENTS_DIR.iterdir() if path.is_file()]
    assert documents
    for document in documents:
        assert document.stat().st_size > 0
