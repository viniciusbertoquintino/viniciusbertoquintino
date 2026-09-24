import { createClient } from "https://esm.sh/@supabase/supabase-js@2.45.0";
import { corsHeaders, jsonResponse } from "../_shared/cors.ts";
import { embed, chat, type ChatMessage } from "../_shared/openai.ts";
import { estimateCost } from "../_shared/cost.ts";

const supabase = createClient(
  Deno.env.get("SUPABASE_URL")!,
  Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!
);

const AGENT_NAMES = {
  analyst: "Document Analyst",
  ticket: "Ticket Assistant",
  workflow: "Workflow Planner",
} as const;

const SYSTEM_PROMPTS = {
  analyst: `Você é o Document Analyst. Analise o input e retorne JSON estrito com este schema:
{
  "steps": [
    {"type":"analysis","content":"resumo executivo (2-3 frases)"},
    {"type":"analysis","content":"pontos-chave em bullets"},
    {"type":"decision","content":"riscos ou pontos de atenção"},
    {"type":"action","content":"FAQ sugerido com 3 perguntas"}
  ],
  "tools_used": ["text_analysis"],
  "confidence": 0.0-1.0
}
Responda apenas com JSON válido.`,
  ticket: `Você é o Ticket Assistant. Use o contexto de políticas (se houver) e analise o ticket. Retorne JSON estrito:
{
  "steps": [
    {"type":"analysis","content":"identificação da política aplicável e citação da fonte"},
    {"type":"decision","content":"prioridade (Baixa/Normal/Alta) e área responsável"},
    {"type":"decision","content":"validação de prazo e cálculos relevantes"},
    {"type":"action","content":"resposta sugerida ao cliente"}
  ],
  "tools_used": ["rag_search","classify_ticket"],
  "confidence": 0.0-1.0
}
Responda apenas com JSON válido.`,
  workflow: `Você é o Workflow Planner. Quebre a solicitação em etapas executáveis usando o contexto fornecido. Retorne JSON estrito:
{
  "steps": [
    {"type":"analysis","content":"entendimento do pedido"},
    {"type":"decision","content":"plano de execução em N passos"},
    {"type":"action","content":"primeiro passo concreto a executar"},
    {"type":"action","content":"próximas ações e tools necessárias"}
  ],
  "tools_used": ["rag_search","planner"],
  "confidence": 0.0-1.0
}
Responda apenas com JSON válido.`,
} as const;

const TAG_VARIANTS = {
  analysis: { tag: "análise", variant: "info" },
  decision: { tag: "decisão", variant: "warn" },
  action: { tag: "ação", variant: "fin" },
} as const;

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response(null, { headers: corsHeaders });
  const t0 = Date.now();

  try {
    const { agent_type, input_text } = await req.json();
    if (!agent_type || !["analyst", "ticket", "workflow"].includes(agent_type)) {
      return jsonResponse({ error: "agent_type must be analyst|ticket|workflow" }, 400);
    }
    if (!input_text || typeof input_text !== "string") {
      return jsonResponse({ error: "input_text required" }, 400);
    }

    const toolsUsed: string[] = [];
    let contextStr = "";
    let embedTokens = 0;

    // RAG retrieval for ticket/workflow
    if (agent_type === "ticket" || agent_type === "workflow") {
      const { embedding, tokens } = await embed(input_text);
      embedTokens = tokens;
      const { data: chunks } = await supabase.rpc("match_document_chunks", {
        query_embedding: `[${embedding.join(",")}]`,
        match_threshold: 0.65,
        match_count: 3,
      });
      const retrieved = (chunks ?? []) as Array<{ document_name: string; content: string; score: number }>;
      if (retrieved.length > 0) {
        toolsUsed.push("document_lookup");
        contextStr =
          "\n\nContexto recuperado dos documentos:\n" +
          retrieved
            .map((c, i) => `[FONTE ${i + 1} — ${c.document_name} (score ${c.score.toFixed(3)})]\n${c.content}`)
            .join("\n\n---\n\n");
      }
    }

    const messages: ChatMessage[] = [
      { role: "system", content: SYSTEM_PROMPTS[agent_type as keyof typeof SYSTEM_PROMPTS] },
      { role: "user", content: `Input:\n${input_text}${contextStr}` },
    ];

    const completion = await chat(messages, { jsonMode: true, temperature: 0.2, maxTokens: 1200 });

    let parsed: { steps?: Array<{ type: string; content: string }>; tools_used?: string[]; confidence?: number };
    try {
      parsed = JSON.parse(completion.content);
    } catch {
      throw new Error("Agent returned invalid JSON");
    }

    const rawSteps = parsed.steps ?? [];
    const steps = rawSteps.map((s, i) => {
      const tv = TAG_VARIANTS[(s.type as keyof typeof TAG_VARIANTS)] ?? TAG_VARIANTS.analysis;
      return {
        number: i + 1,
        title: s.type === "analysis" ? "Análise" : s.type === "decision" ? "Decisão" : "Ação",
        text: s.content,
        tag: tv.tag,
        tagVariant: tv.variant,
      };
    });

    const allTools = Array.from(new Set([...toolsUsed, ...(parsed.tools_used ?? [])]));
    const confidence = typeof parsed.confidence === "number" ? parsed.confidence : 0.8;

    const elapsed = Date.now() - t0;
    const totalTokens = completion.totalTokens + embedTokens;
    const cost =
      estimateCost("gpt-4o-mini", completion.promptTokens, completion.completionTokens) +
      estimateCost("text-embedding-3-small", embedTokens);

    await supabase.from("agent_executions").insert({
      agent_type,
      input_text,
      output_json: { steps, agent_name: AGENT_NAMES[agent_type as keyof typeof AGENT_NAMES] },
      reasoning: parsed,
      tools_used: allTools,
      confidence,
      tokens_used: totalTokens,
      latency_ms: elapsed,
      cost_estimate: cost,
      model: "gpt-4o-mini",
      status: "done",
    });

    return jsonResponse({
      agentName: AGENT_NAMES[agent_type as keyof typeof AGENT_NAMES],
      input: input_text,
      steps,
      tools_used: allTools,
      confidence,
      tokens: totalTokens,
      latency: Number((elapsed / 1000).toFixed(2)),
      cost,
      executedAt: "agora mesmo",
      model: "gpt-4o-mini",
    });
  } catch (err) {
    const msg = err instanceof Error ? err.message : String(err);
    console.error("run-agent error:", msg);
    return jsonResponse({ error: msg }, 500);
  }
});
