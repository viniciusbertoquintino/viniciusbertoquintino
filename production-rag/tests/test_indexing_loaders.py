from pathlib import Path

import pytest
from docx import Document as DocxDocument
from fpdf import FPDF

from app.indexing import load_documents_from_directory


def _create_pdf(path: Path, text: str) -> None:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)
    pdf.multi_cell(0, 10, text)
    pdf.output(str(path))


def test_load_documents_from_directory_routes_supported_suffixes(tmp_path: Path) -> None:
    _create_pdf(tmp_path / "policy.pdf", "PDF content")

    docx_path = tmp_path / "policy.docx"
    document = DocxDocument()
    document.add_paragraph("DOCX content")
    document.save(docx_path)

    (tmp_path / "rows.csv").write_text("a,b\n1,2\n", encoding="utf-8")
    (tmp_path / "notes.txt").write_text("ignored", encoding="utf-8")

    result = load_documents_from_directory(tmp_path)

    assert result.files_processed == 3
    assert len(result.documents) >= 3
    assert result.skipped_files == ["notes.txt"]


def test_load_documents_from_directory_raises_for_missing_path(tmp_path: Path) -> None:
    missing = tmp_path / "missing"

    with pytest.raises(ValueError, match="Input directory does not exist"):
        load_documents_from_directory(missing)
