import time
import json
from typing import Literal
from openai import AsyncOpenAI
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.services.rag_service import generate_embedding, semantic_search

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

AgentType = Literal["analyst", "ticket", "workflow"]

# ─── Prompts ──────────────────────────────────────────────────────────────────

ANALYST_PROMPT = """Você é o Document Analyst, especialista em análise de documentos corporativos.

Dado o texto do documento, produza uma análise estruturada em JSON com:
{
  "summary": "Resumo executivo em 2-3 frases",
  "key_points": ["ponto 1", "ponto 2", "ponto 3"],
  "risks": ["risco 1", "risco 2"],
  "faq": [{"q": "Pergunta frequente?", "a": "Resposta concisa."}],
  "action_items": ["ação 1", "ação 2"]
}

Responda APENAS com o JSON, sem texto adicional."""

TICKET_PROMPT = """Você é o Ticket Assistant, especialista em triagem de chamados corporativos.

Analise o chamado e responda em JSON:
{
  "priority": "Alta|Media|Normal|Baixa",
  "area": "área responsável",
  "category": "categoria do problema",
  "steps": [
    {"number": 1, "title": "...", "text": "...", "tag": "...", "tagVariant": "info|fin|warn|risk"}
  ],
  "suggested_response": "Texto da resposta sugerida ao cliente",
  "sla_hours": 24,
  "churn_risk": true
}

Responda APENAS com o JSON."""

WORKFLOW_PROMPT = """Você é o Workflow Planner, especialista em decompor solicitações complexas em planos de ação.

Analise a solicitação, consulte as políticas disponíveis e produza um plano em JSON:
{
  "objective": "Objetivo principal identificado",
  "steps": [
    {"number": 1, "title": "...", "text": "...", "tag": "...", "tagVariant": "info|fin|warn|risk"}
  ],
  "tools_called": ["ferramenta_1(param)", "ferramenta_2(param)"],
  "recommended_action": "Próxima ação recomendada",
  "estimated_completion": "X dias úteis"
}

Responda APENAS com o JSON."""

PROMPTS = {
    "analyst": ANALYST_PROMPT,
    "ticket": TICKET_PROMPT,
    "workflow": WORKFLOW_PROMPT,
}

AGENT_NAMES = {
    "analyst": "Document Analyst",
    "ticket": "Ticket Assistant",
    "workflow": "Workflow Planner",
}


# ─── Agent Runner ─────────────────────────────────────────────────────────────

async def run_agent(
    agent_type: AgentType,
    input_text: str,
    db: AsyncSession,
) -> dict:
    """
    Run a specialized agent:
    1. Optionally retrieve relevant docs via RAG (ticket, workflow)
    2. Build prompt with context
    3. Call LLM with structured output
    4. Parse and return steps
    """
    t0 = time.time()

    # For ticket and workflow agents, first retrieve relevant policy docs
    rag_context = ""
    if agent_type in ("ticket", "workflow"):
        embedding = await generate_embedding(input_text)
        chunks = await semantic_search(embedding, db, top_k=3, min_score=0.65)
        if chunks:
            parts = [f"[{c['document_name']}]: {c['content'][:300]}..." for c in chunks]
            rag_context = "\n\n".join(parts)

    system_prompt = PROMPTS[agent_type]
    user_content = input_text
    if rag_context:
        user_content = f"Políticas relevantes recuperadas:\n\n{rag_context}\n\n---\n\nSolicitação: {input_text}"

    response = await client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
        temperature=0.2,
        max_tokens=1000,
        response_format={"type": "json_object"},
    )

    raw = response.choices[0].message.content
    result_json = json.loads(raw)
    latency = round(time.time() - t0, 2)

    # Normalize: ensure "steps" key exists for UI rendering
    steps = result_json.get("steps", [])
    if not steps and "key_points" in result_json:
        # Document analyst — convert to steps format
        steps = [
            {"number": 1, "title": "Resumo executivo", "text": result_json.get("summary", ""), "tag": "resumo", "tagVariant": "info"},
            {"number": 2, "title": "Pontos-chave", "text": " · ".join(result_json.get("key_points", [])), "tag": "extração", "tagVariant": "fin"},
            {"number": 3, "title": "Riscos identificados", "text": " · ".join(result_json.get("risks", [])) or "Nenhum risco crítico identificado.", "tag": "riscos", "tagVariant": "risk"},
            {"number": 4, "title": "FAQ gerado", "text": "\n".join(f"Q: {f['q']} A: {f['a']}" for f in result_json.get("faq", [])), "tag": "faq", "tagVariant": "info"},
        ]

    return {
        "agentName": AGENT_NAMES[agent_type],
        "input": input_text,
        "steps": steps,
        "raw": result_json,
        "latency": latency,
        "tokens": response.usage.total_tokens,
        "executedAt": "agora mesmo",
    }
