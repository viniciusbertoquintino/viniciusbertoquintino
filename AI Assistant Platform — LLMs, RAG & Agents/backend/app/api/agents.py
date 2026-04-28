from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.models.models import AgentExecution
from app.services.agent_service import run_agent
import json

router = APIRouter()


class AgentRequest(BaseModel):
    agent_type: str
    input_text: str


@router.post("/run")
async def execute_agent(body: AgentRequest, db: AsyncSession = Depends(get_db)):
    valid = {"analyst", "ticket", "workflow"}
    if body.agent_type not in valid:
        raise HTTPException(400, f"Agent inválido. Use: {valid}")

    result = await run_agent(body.agent_type, body.input_text, db)  # type: ignore

    execution = AgentExecution(
        agent_type=body.agent_type,
        input_text=body.input_text,
        output_json=json.dumps(result),
        tokens_used=result.get("tokens", 0),
        latency_ms=int(result.get("latency", 0) * 1000),
        status="done",
    )
    db.add(execution)
    await db.commit()

    return result


@router.get("/executions")
async def list_executions(limit: int = 20, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(AgentExecution).order_by(AgentExecution.created_at.desc()).limit(limit)
    )
    execs = result.scalars().all()
    return [
        {
            "id": str(e.id),
            "agent_type": e.agent_type,
            "input": e.input_text[:80] + "..." if len(e.input_text) > 80 else e.input_text,
            "tokens": e.tokens_used,
            "latency_ms": e.latency_ms,
            "status": e.status,
            "createdAt": e.created_at,
        }
        for e in execs
    ]
