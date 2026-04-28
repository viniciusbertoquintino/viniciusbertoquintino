import time
import json
from typing import List, Tuple
from openai import AsyncOpenAI
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.core.config import settings

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

RAG_SYSTEM_PROMPT = """Você é um assistente corporativo especializado em responder perguntas com base nos documentos da empresa.

Regras:
- Responda APENAS com base nos documentos fornecidos no contexto
- Seja preciso e cite as informações relevantes
- Se a informação não estiver nos documentos, diga claramente
- Use linguagem profissional e direta
- Organize a resposta de forma clara quando houver múltiplos pontos"""


async def generate_embedding(text: str) -> List[float]:
    """Generate 1536-dim embedding via OpenAI text-embedding-3-small."""
    response = await client.embeddings.create(
        model=settings.EMBEDDING_MODEL,
        input=text,
    )
    return response.data[0].embedding


async def semantic_search(
    query_embedding: List[float],
    db: AsyncSession,
    top_k: int = None,
    min_score: float = None,
) -> List[dict]:
    """
    Cosine similarity search on pgvector.
    Returns chunks sorted by relevance score descending.
    """
    k = top_k or settings.TOP_K_RESULTS
    threshold = min_score or settings.MIN_SIMILARITY_SCORE

    embedding_str = "[" + ",".join(str(v) for v in query_embedding) + "]"

    result = await db.execute(
        text("""
            SELECT
                dc.id,
                dc.content,
                dc.chunk_index,
                d.name AS document_name,
                d.type AS document_type,
                1 - (dc.embedding <=> :embedding::vector) AS score
            FROM document_chunks dc
            JOIN documents d ON dc.document_id = d.id
            WHERE 1 - (dc.embedding <=> :embedding::vector) >= :threshold
            ORDER BY dc.embedding <=> :embedding::vector
            LIMIT :k
        """),
        {"embedding": embedding_str, "threshold": threshold, "k": k},
    )
    return [dict(row) for row in result.mappings()]


async def answer_with_rag(
    query: str,
    db: AsyncSession,
    session_id: str = None,
) -> dict:
    """
    Full RAG pipeline:
    1. Embed query
    2. Retrieve similar chunks
    3. Build context prompt
    4. Generate answer with LLM
    5. Return answer + sources + meta
    """
    t0 = time.time()

    query_embedding = await generate_embedding(query)
    chunks = await semantic_search(query_embedding, db)

    if not chunks:
        return {
            "answer": "Não encontrei informações relevantes nos documentos indexados para responder essa pergunta.",
            "sources": [],
            "meta": {"chunks": 0, "tokens": 0, "latency": round(time.time() - t0, 2)},
        }

    # Build context
    context_parts = []
    for i, chunk in enumerate(chunks):
        context_parts.append(
            f"[FONTE {i+1} — {chunk['document_name']} (score: {chunk['score']:.4f})]\n{chunk['content']}"
        )
    context = "\n\n---\n\n".join(context_parts)

    messages = [
        {"role": "system", "content": RAG_SYSTEM_PROMPT},
        {"role": "user", "content": f"Contexto dos documentos:\n\n{context}\n\nPergunta: {query}"},
    ]

    response = await client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=messages,
        temperature=0.1,
        max_tokens=800,
    )

    answer = response.choices[0].message.content
    latency = round(time.time() - t0, 2)

    sources = [
        {
            "document": c["document_name"],
            "chunk_index": c["chunk_index"],
            "score": round(c["score"], 4),
            "excerpt": c["content"][:200] + "...",
        }
        for c in chunks
    ]

    return {
        "answer": answer,
        "sources": sources,
        "meta": {
            "chunks": len(chunks),
            "tokens": response.usage.total_tokens,
            "prompt_tokens": response.usage.prompt_tokens,
            "completion_tokens": response.usage.completion_tokens,
            "latency": latency,
            "model": settings.OPENAI_MODEL,
        },
    }
