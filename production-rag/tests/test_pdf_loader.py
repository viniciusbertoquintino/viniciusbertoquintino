from pathlib import Path

import pytest
from fpdf import FPDF

from app.ingestion import Document, PDFLoader

SAMPLE_PDF_PATH = Path("data/sample/politica-ferias.pdf")


@pytest.fixture
def sample_pdf(tmp_path: Path) -> Path:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", size=12)
    pdf.multi_cell(0, 10, "Pagina 1: politica de ferias corporativa.")
    pdf.add_page()
    pdf.multi_cell(0, 10, "Pagina 2: agendamento no portal RH.")

    file_path = tmp_path / "politica-ferias.pdf"
    pdf.output(str(file_path))
    return file_path


def test_pdf_loader_extracts_text_filename_and_page(sample_pdf: Path) -> None:
    pages = PDFLoader().load(sample_pdf)

    assert len(pages) == 2
    assert all(isinstance(page, Document) for page in pages)
    assert pages[0].source_type == "pdf"
    assert pages[0].filename == "politica-ferias.pdf"
    assert pages[0].page == 1
    assert "Pagina 1" in pages[0].text
    assert pages[1].filename == "politica-ferias.pdf"
    assert pages[1].page == 2
    assert "Pagina 2" in pages[1].text


def test_pdf_loader_rejects_non_pdf_files(tmp_path: Path) -> None:
    text_file = tmp_path / "documento.txt"
    text_file.write_text("conteudo", encoding="utf-8")

    with pytest.raises(ValueError, match="Expected a PDF file"):
        PDFLoader().load(text_file)


@pytest.mark.skipif(not SAMPLE_PDF_PATH.exists(), reason="sample PDF not available")
def test_pdf_loader_reads_repository_sample_pdf() -> None:
    pages = PDFLoader().load(SAMPLE_PDF_PATH)

    assert pages
    assert pages[0].filename == SAMPLE_PDF_PATH.name
    assert pages[0].page == 1
    assert pages[0].text
