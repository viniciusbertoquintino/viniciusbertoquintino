import { createClient } from "https://esm.sh/@supabase/supabase-js@2.45.0";
import { corsHeaders, jsonResponse } from "../_shared/cors.ts";
import { embed, chat, type ChatMessage } from "../_shared/openai.ts";
import { estimateCost } from "../_shared/cost.ts";
import { overlapScore } from "../_shared/eval.ts";

const supabase = createClient(
  Deno.env.get("SUPABASE_URL")!,
  Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!
);

const SYSTEM_PROMPT = `Você é um assistente corporativo que responde APENAS com base nos documentos fornecidos no contexto.

Regras:
- Use somente as informações do contexto. Se algo não estiver lá, diga claramente.
- Cite as fontes mencionando o nome do documento entre parênteses.
- Seja preciso, profissional e objetivo.
- Organize a resposta com bullets quando houver múltiplos pontos.`;

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response(null, { headers: corsHeaders });
  const t0 = Date.now();

  try {
    const { query, session_id } = await req.json();
    if (!query || typeof query !== "string" || query.trim().length === 0) {
      return jsonResponse({ error: "query is required" }, 400);
    }

    // Ensure session
    let sessionId = session_id as string | undefined;
    if (!sessionId) {
      const { data, error } = await supabase
        .from("chat_sessions")
        .insert({ title: query.slice(0, 60) })
        .select("id")
        .single();
      if (error) throw error;
      sessionId = data.id;
    }

    // Save user msg
    await supabase.from("chat_messages").insert({
      session_id: sessionId,
      role: "user",
      content: query,
    });

    // Embed query
    const { embedding, tokens: embedTokens } = await embed(query);

    // Retrieve
    const { data: chunks, error: matchErr } = await supabase.rpc("match_document_chunks", {
      query_embedding: `[${embedding.join(",")}]`,
      match_threshold: 0.7,
      match_count: 4,
    });
    if (matchErr) throw matchErr;

    const retrieved = (chunks ?? []) as Array<{
      chunk_id: string;
      document_id: string;
      document_name: string;
      chunk_index: number;
      content: string;
      score: number;
    }>;

    // No-context fallback
    if (retrieved.length === 0) {
      const fallback = "Não encontrei informações relevantes nos documentos indexados para responder essa pergunta.";
      const elapsed = Date.now() - t0;
      const embedCost = estimateCost("text-embedding-3-small", embedTokens);
      await supabase.from("chat_messages").insert({
        session_id: sessionId,
        role: "assistant",
        content: fallback,
        sources: [],
        prompt: null,
        tokens_used: embedTokens,
        latency_ms: elapsed,
        cost_estimate: embedCost,
        model: "gpt-4o-mini",
        eval_score: 0,
      });
      return jsonResponse({
        answer: fallback,
        sources: [],
        meta: { tokens: embedTokens, latency: elapsed / 1000, cost: embedCost, model: "gpt-4o-mini", chunks: 0 },
        session_id: sessionId,
      });
    }

    // Memory: last 5 messages (excluding the just-inserted user msg)
    const { data: history } = await supabase
      .from("chat_messages")
      .select("role, content, created_at")
      .eq("session_id", sessionId)
      .order("created_at", { ascending: false })
      .limit(6);
    const memory = (history ?? []).reverse().slice(0, -1); // drop current user msg (latest)

    const contextStr = retrieved
      .map((c, i) => `[FONTE ${i + 1} — ${c.document_name} (score ${c.score.toFixed(3)})]\n${c.content}`)
      .join("\n\n---\n\n");

    const messages: ChatMessage[] = [
      { role: "system", content: SYSTEM_PROMPT },
      ...memory.map((m) => ({ role: m.role as "user" | "assistant", content: m.content })),
      { role: "user", content: `Contexto dos documentos:\n\n${contextStr}\n\nPergunta: ${query}` },
    ];

    const completion = await chat(messages, { temperature: 0.1, maxTokens: 800 });
    const elapsed = Date.now() - t0;

    const sources = retrieved.map((c) => ({
      document: c.document_name,
      score: Number(c.score.toFixed(4)),
      excerpt: c.content.slice(0, 220) + (c.content.length > 220 ? "…" : ""),
      chunk_index: c.chunk_index,
    }));

    const evalScore = overlapScore(completion.content, retrieved.map((c) => c.content));
    const totalTokens = completion.totalTokens + embedTokens;
    const cost =
      estimateCost("gpt-4o-mini", completion.promptTokens, completion.completionTokens) +
      estimateCost("text-embedding-3-small", embedTokens);

    const promptText = messages.map((m) => `[${m.role.toUpperCase()}]\n${m.content}`).join("\n\n");

    await supabase.from("chat_messages").insert({
      session_id: sessionId,
      role: "assistant",
      content: completion.content,
      sources,
      prompt: promptText,
      tokens_used: totalTokens,
      latency_ms: elapsed,
      cost_estimate: cost,
      model: "gpt-4o-mini",
      eval_score: evalScore,
    });

    return jsonResponse({
      answer: completion.content,
      sources,
      meta: {
        tokens: totalTokens,
        latency: elapsed / 1000,
        cost,
        model: "gpt-4o-mini",
        chunks: retrieved.length,
        eval_score: evalScore,
      },
      session_id: sessionId,
    });
  } catch (err) {
    const msg = err instanceof Error ? err.message : String(err);
    console.error("rag-query error:", msg);
    return jsonResponse({ error: msg }, 500);
  }
});
