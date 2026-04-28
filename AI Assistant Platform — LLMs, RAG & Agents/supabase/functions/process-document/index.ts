import { createClient } from "https://esm.sh/@supabase/supabase-js@2.45.0";
import { corsHeaders, jsonResponse } from "../_shared/cors.ts";
import { embedBatch, setOpenAIKey } from "../_shared/openai.ts";
import { estimateCost } from "../_shared/cost.ts";
import { chunkText } from "../_shared/chunker.ts";
import { normalize, sha256Hex } from "../_shared/text.ts";

const supabase = createClient(
  Deno.env.get("SUPABASE_URL")!,
  Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!
);

async function extractText(blob: Blob, type: string): Promise<string> {
  const lower = type.toLowerCase();
  if (lower === "txt" || lower === "md") {
    return await blob.text();
  }
  // PDF/DOCX/XLSX MVP fallback: try utf-8 decode and strip non-text.
  // Real parsers are a follow-up.
  try {
    const raw = await blob.text();
    return raw.replace(/[^\x09\x0A\x0D\x20-\x7E\u00A0-\uFFFF]+/g, " ");
  } catch {
    return "";
  }
}

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response(null, { headers: corsHeaders });

  const t0 = Date.now();
  let documentId: string | undefined;

  try {
    const body = await req.json();
    documentId = body.document_id;
    const storagePath: string = body.storage_path;
    const openaiApiKey: string | undefined = body.openai_api_key || Deno.env.get("OPENAI_API_KEY");
    if (!documentId || !storagePath) {
      return jsonResponse({ error: "document_id and storage_path required" }, 400);
    }
    if (!openaiApiKey) {
      return jsonResponse({ error: "OpenAI API key não configurada. Acesse Configurações para inserir sua chave." }, 400);
    }
    setOpenAIKey(openaiApiKey);

    // Cache: skip if already indexed
    const { data: doc } = await supabase
      .from("documents")
      .select("id, status, type, content_hash")
      .eq("id", documentId)
      .single();
    if (!doc) return jsonResponse({ error: "document not found" }, 404);
    if (doc.status === "indexado") {
      return jsonResponse({ ok: true, cached: true, document_id: documentId });
    }

    await supabase.from("documents").update({ status: "processando" }).eq("id", documentId);

    // Download
    const { data: file, error: dlErr } = await supabase.storage.from("documents").download(storagePath);
    if (dlErr || !file) throw new Error(`download failed: ${dlErr?.message}`);

    // Extract + normalize
    const rawText = await extractText(file, doc.type);
    const text = normalize(rawText);
    if (!text || text.length < 1) {
      throw new Error("Arquivo vazio ou sem conteúdo legível.");
    }

    const hash = await sha256Hex(text);

    // Dedupe: another indexed document with same hash
    const { data: dupe } = await supabase
      .from("documents")
      .select("id, chunks_count, tokens_count, avg_score")
      .eq("content_hash", hash)
      .eq("status", "indexado")
      .neq("id", documentId)
      .maybeSingle();

    if (dupe) {
      await supabase
        .from("documents")
        .update({
          status: "indexado",
          content_hash: hash,
          chunks_count: dupe.chunks_count,
          tokens_count: dupe.tokens_count,
          avg_score: dupe.avg_score,
          processing_time_ms: Date.now() - t0,
        })
        .eq("id", documentId);
      return jsonResponse({ ok: true, deduped: true, document_id: documentId });
    }

    // Chunk
    const chunks = chunkText(text);

    // Embed in batches of 96
    let totalEmbeddingTokens = 0;
    const chunkRows: Array<{
      document_id: string;
      chunk_index: number;
      content: string;
      embedding: string;
      tokens: number;
    }> = [];

    const BATCH = 96;
    for (let i = 0; i < chunks.length; i += BATCH) {
      const batch = chunks.slice(i, i + BATCH);
      const { embeddings, tokens } = await embedBatch(batch.map((c) => c.content));
      totalEmbeddingTokens += tokens;
      batch.forEach((c, j) => {
        chunkRows.push({
          document_id: documentId!,
          chunk_index: i + j,
          content: c.content,
          embedding: `[${embeddings[j].join(",")}]`,
          tokens: c.tokens,
        });
      });
    }

    // Insert chunks (in batches to avoid row limit)
    const INSERT_BATCH = 100;
    for (let i = 0; i < chunkRows.length; i += INSERT_BATCH) {
      const slice = chunkRows.slice(i, i + INSERT_BATCH);
      const { error } = await supabase.from("document_chunks").insert(slice);
      if (error) throw new Error(`chunk insert failed: ${error.message}`);
    }

    const elapsed = Date.now() - t0;
    await supabase
      .from("documents")
      .update({
        status: "indexado",
        content_hash: hash,
        chunks_count: chunks.length,
        tokens_count: totalEmbeddingTokens,
        processing_time_ms: elapsed,
        processing_error: null,
      })
      .eq("id", documentId);

    return jsonResponse({
      ok: true,
      document_id: documentId,
      chunks: chunks.length,
      tokens: totalEmbeddingTokens,
      cost: estimateCost("text-embedding-3-small", totalEmbeddingTokens),
      latency_ms: elapsed,
    });
  } catch (err) {
    const msg = err instanceof Error ? err.message : String(err);
    console.error("process-document error:", msg);
    if (documentId) {
      await supabase
        .from("documents")
        .update({ status: "erro", processing_error: msg, processing_time_ms: Date.now() - t0 })
        .eq("id", documentId);
    }
    return jsonResponse({ error: msg }, 500);
  }
});
