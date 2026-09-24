from pathlib import Path

import pytest
from openpyxl import Workbook

from app.ingestion import Document, TabularLoader

SAMPLE_CSV_PATH = Path("data/sample/processo-reembolso-despesas.csv")
SAMPLE_XLSX_PATH = Path("data/sample/sla-suporte-interno.xlsx")


@pytest.fixture
def sample_csv(tmp_path: Path) -> Path:
    file_path = tmp_path / "reembolsos.csv"
    file_path.write_text(
        "categoria,descricao,valor\n"
        "transporte,taxi aeroporto,85.50\n"
        "alimentacao,almoco viagem,72.00\n",
        encoding="utf-8",
    )
    return file_path


@pytest.fixture
def sample_xlsx(tmp_path: Path) -> Path:
    file_path = tmp_path / "sla-suporte.xlsx"
    workbook = Workbook()
    priorities = workbook.active
    priorities.title = "Prioridades"
    priorities.append(["prioridade", "descricao", "tempo_resposta"])
    priorities.append(["P1", "Sistema critico indisponivel", "30 minutos"])
    priorities.append(["P2", "Degradacao relevante", "4 horas"])

    escalation = workbook.create_sheet("Escalonamento")
    escalation.append(["condicao", "acao"])
    escalation.append(["P1 sem resposta em 30 min", "Escalar plantonista"])

    workbook.save(file_path)
    return file_path


def test_tabular_loader_extracts_traceable_csv_rows(sample_csv: Path) -> None:
    rows = TabularLoader().load(sample_csv)

    assert len(rows) == 2
    assert all(isinstance(row, Document) for row in rows)
    assert rows[0].source_type == "csv"
    assert rows[0].filename == "reembolsos.csv"
    assert rows[0].sheet is None
    assert rows[0].row == 2
    assert rows[0].text == "categoria: transporte | descricao: taxi aeroporto | valor: 85.50"
    assert rows[1].row == 3
    assert "alimentacao" in rows[1].text


def test_tabular_loader_extracts_traceable_xlsx_rows_by_sheet(sample_xlsx: Path) -> None:
    rows = TabularLoader().load(sample_xlsx)

    assert len(rows) == 3
    assert rows[0].source_type == "xlsx"
    assert rows[0].filename == "sla-suporte.xlsx"
    assert rows[0].sheet == "Prioridades"
    assert rows[0].row == 2
    assert "P1" in rows[0].text
    assert rows[1].sheet == "Prioridades"
    assert rows[1].row == 3
    assert rows[2].sheet == "Escalonamento"
    assert rows[2].row == 2
    assert "Escalar plantonista" in rows[2].text


def test_tabular_loader_rejects_unsupported_files(tmp_path: Path) -> None:
    text_file = tmp_path / "documento.txt"
    text_file.write_text("conteudo", encoding="utf-8")

    with pytest.raises(ValueError, match="Expected a CSV or XLSX file"):
        TabularLoader().load(text_file)


@pytest.mark.skipif(not SAMPLE_CSV_PATH.exists(), reason="sample CSV not available")
def test_tabular_loader_reads_repository_sample_csv() -> None:
    rows = TabularLoader().load(SAMPLE_CSV_PATH)

    assert rows
    assert rows[0].filename == SAMPLE_CSV_PATH.name
    assert rows[0].sheet is None
    assert rows[0].row >= 2
    assert rows[0].text


@pytest.mark.skipif(not SAMPLE_XLSX_PATH.exists(), reason="sample XLSX not available")
def test_tabular_loader_reads_repository_sample_xlsx() -> None:
    rows = TabularLoader().load(SAMPLE_XLSX_PATH)

    assert rows
    assert rows[0].filename == SAMPLE_XLSX_PATH.name
    assert rows[0].sheet
    assert rows[0].row >= 2
    assert rows[0].text
