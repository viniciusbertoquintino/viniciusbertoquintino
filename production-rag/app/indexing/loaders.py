from pathlib import Path

from app.indexing.models import DirectoryLoadResult
from app.ingestion import Document, DOCXLoader, PDFLoader, TabularLoader

SUPPORTED_SUFFIXES = {".pdf", ".docx", ".csv", ".xlsx"}


def load_documents_from_directory(path: Path) -> DirectoryLoadResult:
    """Load supported documents from a directory, skipping unknown file types."""
    if not path.is_dir():
        raise ValueError(f"Input directory does not exist: {path}")

    pdf_loader = PDFLoader()
    docx_loader = DOCXLoader()
    tabular_loader = TabularLoader()

    documents: list[Document] = []
    skipped_files: list[str] = []
    files_processed = 0

    for file_path in sorted(path.iterdir()):
        if not file_path.is_file():
            continue

        suffix = file_path.suffix.lower()
        if suffix not in SUPPORTED_SUFFIXES:
            skipped_files.append(file_path.name)
            continue

        if suffix == ".pdf":
            documents.extend(pdf_loader.load(file_path))
        elif suffix == ".docx":
            documents.extend(docx_loader.load(file_path))
        elif suffix in {".csv", ".xlsx"}:
            documents.extend(tabular_loader.load(file_path))

        files_processed += 1

    return DirectoryLoadResult(
        documents=documents,
        files_processed=files_processed,
        skipped_files=skipped_files,
    )
