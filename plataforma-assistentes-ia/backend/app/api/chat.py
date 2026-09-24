import uuid
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.models.models import ChatSession, ChatMessage
from app.services.rag_service import answer_with_rag
import json

router = APIRouter()


class QueryRequest(BaseModel):
    query: str
    session_id: str | None = None


@router.post("/query")
async def chat_query(body: QueryRequest, db: AsyncSession = Depends(get_db)):
    if not body.query.strip():
        raise HTTPException(400, "Query não pode ser vazia")

    result = await answer_with_rag(body.query, db, body.session_id)

    # Persist session + messages
    session_id = body.session_id or str(uuid.uuid4())
    session = await db.get(ChatSession, session_id)
    if not session:
        session = ChatSession(id=session_id, title=body.query[:60])
        db.add(session)

    user_msg = ChatMessage(session_id=session_id, role="user", content=body.query)
    ai_msg = ChatMessage(
        session_id=session_id,
        role="assistant",
        content=result["answer"],
        sources=json.dumps(result["sources"]),
        tokens_used=result["meta"].get("tokens", 0),
        latency_ms=int(result["meta"].get("latency", 0) * 1000),
    )
    db.add(user_msg)
    db.add(ai_msg)
    await db.commit()

    return {
        "session_id": session_id,
        "answer": result["answer"],
        "sources": result["sources"],
        "meta": result["meta"],
    }


@router.get("/sessions")
async def list_sessions(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(ChatSession).order_by(ChatSession.created_at.desc()).limit(20)
    )
    sessions = result.scalars().all()
    return [{"id": str(s.id), "title": s.title, "createdAt": s.created_at} for s in sessions]


@router.get("/sessions/{session_id}/messages")
async def get_messages(session_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(ChatMessage)
        .where(ChatMessage.session_id == session_id)
        .order_by(ChatMessage.created_at)
    )
    msgs = result.scalars().all()
    return [
        {
            "id": str(m.id),
            "role": m.role,
            "content": m.content,
            "sources": json.loads(m.sources) if m.sources else [],
            "timestamp": m.created_at,
        }
        for m in msgs
    ]
