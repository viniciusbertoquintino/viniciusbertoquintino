let _runtimeKey: string | undefined;
export function setOpenAIKey(key: string) { _runtimeKey = key; }
function getKey(): string {
  return _runtimeKey || Deno.env.get("OPENAI_API_KEY") || "";
}

async function withRetry<T>(fn: () => Promise<Response>, maxRetries = 2): Promise<Response> {
  let lastErr: unknown;
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      const res = await fn();
      if (res.status === 429 || res.status >= 500) {
        if (attempt < maxRetries) {
          await new Promise((r) => setTimeout(r, 500 * Math.pow(2, attempt)));
          continue;
        }
      }
      return res;
    } catch (err) {
      lastErr = err;
      if (attempt < maxRetries) {
        await new Promise((r) => setTimeout(r, 500 * Math.pow(2, attempt)));
        continue;
      }
    }
  }
  throw lastErr ?? new Error("OpenAI request failed");
}

export async function embedBatch(inputs: string[]): Promise<{ embeddings: number[][]; tokens: number }> {
  if (inputs.length === 0) return { embeddings: [], tokens: 0 };
  const res = await withRetry(() =>
    fetch("https://api.openai.com/v1/embeddings", {
      method: "POST",
      headers: { Authorization: `Bearer ${getKey()}`, "Content-Type": "application/json" },
      body: JSON.stringify({ model: "text-embedding-3-small", input: inputs }),
    })
  );
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Embedding API error ${res.status}: ${text}`);
  }
  const data = await res.json();
  return {
    embeddings: data.data.map((d: { embedding: number[] }) => d.embedding),
    tokens: data.usage?.total_tokens ?? 0,
  };
}

export async function embed(text: string): Promise<{ embedding: number[]; tokens: number }> {
  const { embeddings, tokens } = await embedBatch([text]);
  return { embedding: embeddings[0], tokens };
}

export interface ChatMessage {
  role: "system" | "user" | "assistant";
  content: string;
}

export async function chat(
  messages: ChatMessage[],
  opts: { jsonMode?: boolean; temperature?: number; maxTokens?: number } = {}
): Promise<{ content: string; promptTokens: number; completionTokens: number; totalTokens: number }> {
  const body: Record<string, unknown> = {
    model: "gpt-4o-mini",
    messages,
    temperature: opts.temperature ?? 0.2,
    max_tokens: opts.maxTokens ?? 1000,
  };
  if (opts.jsonMode) body.response_format = { type: "json_object" };

  const res = await withRetry(() =>
    fetch("https://api.openai.com/v1/chat/completions", {
      method: "POST",
      headers: { Authorization: `Bearer ${getKey()}`, "Content-Type": "application/json" },
      body: JSON.stringify(body),
    })
  );
  if (!res.ok) {
    const text = await res.text();
    throw new Error(`Chat API error ${res.status}: ${text}`);
  }
  const data = await res.json();
  return {
    content: data.choices[0].message.content,
    promptTokens: data.usage?.prompt_tokens ?? 0,
    completionTokens: data.usage?.completion_tokens ?? 0,
    totalTokens: data.usage?.total_tokens ?? 0,
  };
}
