import json
from datetime import datetime
from unittest.mock import AsyncMock, patch

from app.models.models import AgentExecution

AGENT_RESULT = {
    "agentName": "Document Analyst",
    "input": "analise este texto",
    "steps": [{"number": 1, "title": "Resumo executivo", "text": "Resumo"}],
    "raw": {"summary": "Resumo"},
    "latency": 0.5,
    "tokens": 30,
    "executedAt": "agora mesmo",
}


def test_run_rejects_unknown_agent(client, db):
    with patch("app.api.agents.run_agent", new_callable=AsyncMock) as run:
        response = client.post(
            "/api/v1/agents/run",
            json={"agent_type": "outro", "input_text": "texto"},
        )

    assert response.status_code == 400
    assert "Agent inválido" in response.json()["detail"]
    run.assert_not_awaited()
    assert db.added == []


def test_run_persists_execution(client, db):
    with patch("app.api.agents.run_agent", new_callable=AsyncMock) as run:
        run.return_value = AGENT_RESULT
        response = client.post(
            "/api/v1/agents/run",
            json={"agent_type": "analyst", "input_text": "analise este texto"},
        )

    assert response.status_code == 200
    assert response.json() == AGENT_RESULT
    run.assert_awaited_once()
    assert run.await_args.args[0] == "analyst"
    assert run.await_args.args[1] == "analise este texto"
    assert run.await_args.args[2] is db

    assert len(db.added) == 1
    execution = db.added[0]
    assert isinstance(execution, AgentExecution)
    assert execution.agent_type == "analyst"
    assert execution.input_text == "analise este texto"
    assert json.loads(execution.output_json) == AGENT_RESULT
    assert execution.tokens_used == 30
    assert execution.latency_ms == 500
    assert execution.status == "done"
    assert db.committed == 1


def test_list_executions_truncates_long_input(client, db):
    long_input = "a" * 90
    db.query_rows = [
        AgentExecution(
            id="22222222-2222-2222-2222-222222222222",
            agent_type="ticket",
            input_text=long_input,
            tokens_used=8,
            latency_ms=100,
            status="done",
            created_at=datetime(2026, 3, 15, 14, 30),
        ),
        AgentExecution(
            id="66666666-6666-6666-6666-666666666666",
            agent_type="workflow",
            input_text="curto",
            tokens_used=4,
            latency_ms=50,
            status="done",
            created_at=datetime(2026, 3, 15, 15, 0),
        ),
    ]

    response = client.get("/api/v1/agents/executions")

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": "22222222-2222-2222-2222-222222222222",
            "agent_type": "ticket",
            "input": f"{'a' * 80}...",
            "tokens": 8,
            "latency_ms": 100,
            "status": "done",
            "createdAt": "2026-03-15T14:30:00",
        },
        {
            "id": "66666666-6666-6666-6666-666666666666",
            "agent_type": "workflow",
            "input": "curto",
            "tokens": 4,
            "latency_ms": 50,
            "status": "done",
            "createdAt": "2026-03-15T15:00:00",
        },
    ]
