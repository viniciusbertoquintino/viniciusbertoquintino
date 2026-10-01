import json
from datetime import datetime
from unittest.mock import AsyncMock, patch

from app.models.models import ChatMessage, ChatSession

RAG_RESULT = {
    "answer": "A política permite home office.",
    "sources": [
        {
            "document": "politica.md",
            "chunk_index": 0,
            "score": 0.91,
            "excerpt": "Home office...",
        }
    ],
    "meta": {"chunks": 1, "tokens": 12, "latency": 0.2},
}


def test_query_rejects_blank_text(client, db):
    with patch("app.api.chat.answer_with_rag", new_callable=AsyncMock) as rag:
        response = client.post("/api/v1/chat/query", json={"query": "   "})

    assert response.status_code == 400
    assert response.json()["detail"] == "Query não pode ser vazia"
    rag.assert_not_awaited()
    assert db.committed == 0


def test_query_persists_new_session_and_messages(client, db):
    with patch("app.api.chat.answer_with_rag", new_callable=AsyncMock) as rag:
        rag.return_value = RAG_RESULT
        response = client.post(
            "/api/v1/chat/query",
            json={"query": "qual a política?"},
        )

    assert response.status_code == 200
    body = response.json()
    assert body["answer"] == RAG_RESULT["answer"]
    assert body["sources"] == RAG_RESULT["sources"]
    assert body["meta"] == RAG_RESULT["meta"]
    assert body["session_id"]
    rag.assert_awaited_once()
    assert rag.await_args.args[0] == "qual a política?"
    assert rag.await_args.args[1] is db
    assert rag.await_args.args[2] is None

    sessions = [obj for obj in db.added if isinstance(obj, ChatSession)]
    messages = [obj for obj in db.added if isinstance(obj, ChatMessage)]
    assert len(sessions) == 1
    assert sessions[0].id == body["session_id"]
    assert sessions[0].title == "qual a política?"
    assert [message.role for message in messages] == ["user", "assistant"]
    assert messages[0].content == "qual a política?"
    assert messages[1].content == RAG_RESULT["answer"]
    assert json.loads(messages[1].sources) == RAG_RESULT["sources"]
    assert messages[1].tokens_used == 12
    assert messages[1].latency_ms == 200
    assert db.committed == 1


def test_query_reuses_existing_session(client, db):
    session_id = "33333333-3333-3333-3333-333333333333"
    db.remember(
        ChatSession,
        ChatSession(id=session_id, title="antiga", created_at=datetime(2026, 3, 15, 14, 0)),
    )

    with patch("app.api.chat.answer_with_rag", new_callable=AsyncMock) as rag:
        rag.return_value = RAG_RESULT
        response = client.post(
            "/api/v1/chat/query",
            json={"query": "de novo", "session_id": session_id},
        )

    assert response.status_code == 200
    assert response.json()["session_id"] == session_id
    assert rag.await_args.args[2] == session_id
    assert not any(isinstance(obj, ChatSession) for obj in db.added)
    assert len([obj for obj in db.added if isinstance(obj, ChatMessage)]) == 2


def test_list_sessions(client, db):
    created_at = datetime(2026, 3, 15, 14, 30)
    db.query_rows = [
        ChatSession(
            id="33333333-3333-3333-3333-333333333333",
            title="Política",
            created_at=created_at,
        )
    ]

    response = client.get("/api/v1/chat/sessions")

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": "33333333-3333-3333-3333-333333333333",
            "title": "Política",
            "createdAt": "2026-03-15T14:30:00",
        }
    ]


def test_list_messages_parses_sources(client, db):
    created_at = datetime(2026, 3, 15, 14, 31)
    db.query_rows = [
        ChatMessage(
            id="44444444-4444-4444-4444-444444444444",
            session_id="33333333-3333-3333-3333-333333333333",
            role="user",
            content="oi",
            sources=None,
            created_at=created_at,
        ),
        ChatMessage(
            id="55555555-5555-5555-5555-555555555555",
            session_id="33333333-3333-3333-3333-333333333333",
            role="assistant",
            content="olá",
            sources=json.dumps([{"document": "politica.md"}]),
            created_at=created_at,
        ),
    ]

    response = client.get(
        "/api/v1/chat/sessions/33333333-3333-3333-3333-333333333333/messages"
    )

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": "44444444-4444-4444-4444-444444444444",
            "role": "user",
            "content": "oi",
            "sources": [],
            "timestamp": "2026-03-15T14:31:00",
        },
        {
            "id": "55555555-5555-5555-5555-555555555555",
            "role": "assistant",
            "content": "olá",
            "sources": [{"document": "politica.md"}],
            "timestamp": "2026-03-15T14:31:00",
        },
    ]
