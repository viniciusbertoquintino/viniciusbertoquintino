from pathlib import Path

from pypdf import PdfReader

from app.ingestion.models import Document


class PDFLoader:
    """Load text content from PDF files page by page."""

    def load(self, file_path: Path) -> list[Document]:
        if file_path.suffix.lower() != ".pdf":
            raise ValueError(f"Expected a PDF file, got: {file_path.name}")

        reader = PdfReader(str(file_path))
        pages: list[Document] = []

        for page_number, page in enumerate(reader.pages, start=1):
            text = page.extract_text() or ""
            pages.append(
                Document(
                    filename=file_path.name,
                    source_type="pdf",
                    text=text.strip(),
                    page=page_number,
                )
            )

        return pages
