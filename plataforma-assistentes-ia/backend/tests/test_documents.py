from datetime import datetime
from unittest.mock import AsyncMock, patch

from app.models.models import Document, DocumentStatus


def make_document(**overrides):
    data = {
        "id": "11111111-1111-1111-1111-111111111111",
        "name": "politica.txt",
        "type": "txt",
        "status": DocumentStatus.INDEXED,
        "size_bytes": 2048,
        "chunks_count": 3,
        "tokens_count": 120,
        "created_at": datetime(2026, 3, 15, 14, 30),
    }
    data.update(overrides)
    return Document(**data)


def test_upload_queues_supported_file(client, db):
    with patch("app.api.documents.process_document", new_callable=AsyncMock) as process:
        response = client.post(
            "/api/v1/documents/upload",
            files={"file": ("Nota.TXT", b"ola mundo", "text/plain")},
        )

    assert response.status_code == 200
    body = response.json()
    assert body["name"] == "Nota.TXT"
    assert body["status"] == "na_fila"
    assert db.committed == 1
    assert len(db.added) == 1
    assert db.added[0].type == "txt"
    assert db.added[0].status == DocumentStatus.QUEUED
    assert db.added[0].size_bytes == len(b"ola mundo")
    process.assert_awaited_once()
    doc_id, file_bytes, ext, session = process.await_args.args
    assert doc_id == body["id"]
    assert file_bytes == b"ola mundo"
    assert ext == "txt"
    assert session is db


def test_upload_rejects_unsupported_type(client, db):
    with patch("app.api.documents.process_document", new_callable=AsyncMock) as process:
        response = client.post(
            "/api/v1/documents/upload",
            files={"file": ("virus.exe", b"bin", "application/octet-stream")},
        )

    assert response.status_code == 400
    assert "exe" in response.json()["detail"]
    assert db.added == []
    process.assert_not_awaited()


def test_list_documents_serializes_rows(client, db):
    db.query_rows = [make_document()]

    response = client.get("/api/v1/documents/")

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": "11111111-1111-1111-1111-111111111111",
            "name": "politica.txt",
            "type": "txt",
            "status": "indexado",
            "chunks": 3,
            "tokens": 120,
            "size": "2 KB",
            "uploadedAt": "15/03/2026 14:30",
        }
    ]


def test_list_documents_is_empty(client):
    response = client.get("/api/v1/documents/")

    assert response.status_code == 200
    assert response.json() == []


def test_get_document_returns_metadata(client, db):
    doc = make_document()
    db.remember(Document, doc)

    response = client.get(f"/api/v1/documents/{doc.id}")

    assert response.status_code == 200
    assert response.json() == {
        "id": "11111111-1111-1111-1111-111111111111",
        "name": "politica.txt",
        "type": "txt",
        "status": "indexado",
        "chunks": 3,
        "tokens": 120,
    }


def test_get_document_returns_404(client):
    response = client.get("/api/v1/documents/inexistente")

    assert response.status_code == 404
    assert response.json()["detail"] == "Documento não encontrado"


def test_delete_document_removes_existing_row(client, db):
    doc = make_document()
    db.remember(Document, doc)

    response = client.delete(f"/api/v1/documents/{doc.id}")

    assert response.status_code == 200
    assert response.json() == {"deleted": str(doc.id)}
    assert db.deleted == [doc]
    assert db.committed == 1


def test_delete_document_returns_404(client, db):
    response = client.delete("/api/v1/documents/inexistente")

    assert response.status_code == 404
    assert response.json()["detail"] == "Documento não encontrado"
    assert db.deleted == []
    assert db.committed == 0
