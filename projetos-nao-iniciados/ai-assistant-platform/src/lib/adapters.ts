import type { Document, LogEntry, Source } from "@/types";

function relativeTime(iso: string): string {
  const diff = Date.now() - new Date(iso).getTime();
  const m = Math.floor(diff / 60000);
  if (m < 1) return "agora";
  if (m < 60) return `${m} min atrás`;
  const h = Math.floor(m / 60);
  if (h < 24) return `${h}h atrás`;
  const d = Math.floor(h / 24);
  return `${d}d atrás`;
}

function formatSize(bytes: number): string {
  if (!bytes) return "—";
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(0)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

export interface DocumentRow {
  id: string;
  name: string;
  type: string;
  status: string;
  chunks_count: number | null;
  tokens_count: number | null;
  avg_score: number | null;
  size_bytes: number | null;
  created_at: string;
  processing_error?: string | null;
}

export function rowToDocument(r: DocumentRow): Document {
  return {
    id: r.id,
    name: r.name,
    type: (["pdf", "docx", "xlsx", "txt", "md"].includes(r.type) ? r.type : "txt") as Document["type"],
    status: (r.status as Document["status"]) ?? "na_fila",
    chunks: r.chunks_count ?? 0,
    tokens: r.tokens_count ?? 0,
    score: r.avg_score ?? 0,
    size: formatSize(r.size_bytes ?? 0),
    uploadedAt: relativeTime(r.created_at),
    processingError: r.processing_error ?? undefined,
  };
}

interface ChatLogRow {
  id: string;
  created_at: string;
  content: string;
  prompt: string | null;
  tokens_used: number | null;
  latency_ms: number | null;
  sources: unknown;
  chat_sessions?: { title: string | null } | null;
}
interface AgentLogRow {
  id: string;
  created_at: string;
  agent_type: string;
  input_text: string;
  reasoning: unknown;
  tools_used: unknown;
  tokens_used: number | null;
  latency_ms: number | null;
  status: string | null;
}
interface DocLogRow {
  id: string;
  created_at: string;
  name: string;
  chunks_count: number | null;
  tokens_count: number | null;
  processing_time_ms: number | null;
  status: string;
  processing_error: string | null;
}

function fmtTime(iso: string): string {
  const d = new Date(iso);
  return d.toLocaleTimeString("pt-BR", { hour: "2-digit", minute: "2-digit" });
}

export function chatToLog(m: ChatLogRow): LogEntry {
  const sources = Array.isArray(m.sources) ? (m.sources as Source[]) : [];
  return {
    id: m.id,
    timestamp: fmtTime(m.created_at),
    type: "RAG",
    operation: m.chat_sessions?.title || m.content.slice(0, 60),
    tokens: m.tokens_used ?? 0,
    latency: (m.latency_ms ?? 0) / 1000,
    docs: sources.length,
    status: "ok",
    promptSent: m.prompt ?? undefined,
    retrievedChunks: sources.map(
      (s) => `📄 ${s.document} · score ${typeof s.score === "number" ? s.score.toFixed(4) : s.score}`
    ),
  };
}

export function agentToLog(a: AgentLogRow): LogEntry {
  const tools = Array.isArray(a.tools_used) ? (a.tools_used as string[]) : [];
  const reasoning = a.reasoning && typeof a.reasoning === "object" ? JSON.stringify(a.reasoning, null, 2) : undefined;
  return {
    id: a.id,
    timestamp: fmtTime(a.created_at),
    type: "AGENT",
    operation: `${a.agent_type} — ${a.input_text.slice(0, 60)}`,
    tokens: a.tokens_used ?? 0,
    latency: (a.latency_ms ?? 0) / 1000,
    docs: tools.includes("document_lookup") ? 3 : null,
    status: a.status === "erro" ? "error" : "ok",
    promptSent: reasoning,
    toolsCalled: tools.map((t) => `🔧 ${t}`),
  };
}

export function docToLog(d: DocLogRow): LogEntry {
  return {
    id: d.id,
    timestamp: fmtTime(d.created_at),
    type: "EMBED",
    operation: `${d.name} — ${d.chunks_count ?? 0} chunks`,
    tokens: d.tokens_count ?? 0,
    latency: (d.processing_time_ms ?? 0) / 1000,
    docs: null,
    status: d.status === "erro" ? "error" : "ok",
    warning: d.processing_error ?? undefined,
  };
}
