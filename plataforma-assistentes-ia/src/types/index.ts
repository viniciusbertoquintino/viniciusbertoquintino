// ─── Documents ───────────────────────────────────────────────────────────────

export type DocumentStatus = "indexado" | "processando" | "erro" | "na_fila";
export type DocumentType = "pdf" | "docx" | "xlsx" | "txt" | "md";

export interface Document {
  id: string;
  name: string;
  type: DocumentType;
  status: DocumentStatus;
  chunks: number;
  tokens: number;
  score: number;
  size: string;
  uploadedAt: string;
  processingError?: string;
}

// ─── Chat / RAG ───────────────────────────────────────────────────────────────

export interface Source {
  document: string;
  page?: string | number;
  section?: string;
  score: number;
  excerpt: string;
}

export interface Message {
  id: string;
  role: "user" | "assistant";
  content: string;
  sources?: Source[];
  meta?: {
    chunks: number;
    tokens: number;
    latency: number;
    model: string;
  };
  timestamp: string;
}

export interface ChatSession {
  id: string;
  title: string;
  messages: Message[];
  createdAt: string;
}

// ─── Agents ───────────────────────────────────────────────────────────────────

export type AgentType = "analyst" | "ticket" | "workflow";
export type AgentStatus = "ready" | "running" | "done" | "error";

export interface AgentCapability {
  label: string;
}

export interface AgentConfig {
  id: AgentType;
  name: string;
  description: string;
  capabilities: string[];
  colorClass: string;
  emoji: string;
}

export interface AgentStep {
  number: number;
  title: string;
  text: string;
  tag: string;
  tagVariant: "fin" | "risk" | "info" | "warn";
}

export interface AgentResult {
  agentName: string;
  input: string;
  steps: AgentStep[];
  latency: number;
  tokens: number;
  executedAt: string;
}

// ─── Logs ────────────────────────────────────────────────────────────────────

export type LogType = "RAG" | "AGENT" | "EMBED";
export type LogStatus = "ok" | "warn" | "error";

export interface LogEntry {
  id: string;
  timestamp: string;
  type: LogType;
  operation: string;
  tokens: number;
  latency: number;
  docs: number | null;
  status: LogStatus;
  promptSent?: string;
  retrievedChunks?: string[];
  toolsCalled?: string[];
  warning?: string;
}

// ─── Metrics ─────────────────────────────────────────────────────────────────

export interface PlatformMetrics {
  documentsIndexed: number;
  ragQueries: number;
  tokensToday: number;
  avgLatency: number;
  estimatedCost: number;
  successRate: number;
}
