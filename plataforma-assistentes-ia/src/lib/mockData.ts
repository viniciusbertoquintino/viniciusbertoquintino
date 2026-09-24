import type {
  Document,
  Message,
  AgentConfig,
  AgentResult,
  LogEntry,
  PlatformMetrics,
} from "@/types";

// ─── Platform Metrics ────────────────────────────────────────────────────────

export const mockMetrics: PlatformMetrics = {
  documentsIndexed: 1284,
  ragQueries: 8421,
  tokensToday: 412000,
  avgLatency: 1.2,
  estimatedCost: 12.4,
  successRate: 99.2,
};

// ─── Documents ───────────────────────────────────────────────────────────────

export const mockDocuments: Document[] = [
  {
    id: "doc-001",
    name: "politica-reembolso-2024.pdf",
    type: "pdf",
    status: "indexado",
    chunks: 247,
    tokens: 18400,
    score: 0.92,
    size: "1.2 MB",
    uploadedAt: "2h atrás",
  },
  {
    id: "doc-002",
    name: "manual-rh-v3.docx",
    type: "docx",
    status: "processando",
    chunks: 612,
    tokens: 47200,
    score: 0,
    size: "3.8 MB",
    uploadedAt: "5h atrás",
  },
  {
    id: "doc-003",
    name: "tabela-precos-q4.xlsx",
    type: "xlsx",
    status: "na_fila",
    chunks: 89,
    tokens: 6100,
    score: 0,
    size: "540 KB",
    uploadedAt: "1d atrás",
  },
  {
    id: "doc-004",
    name: "contrato-fornecedor-xyz.pdf",
    type: "pdf",
    status: "indexado",
    chunks: 333,
    tokens: 24800,
    score: 0.88,
    size: "2.1 MB",
    uploadedAt: "2d atrás",
  },
  {
    id: "doc-005",
    name: "politica-ferias-2024.pdf",
    type: "pdf",
    status: "indexado",
    chunks: 98,
    tokens: 7300,
    score: 0.91,
    size: "780 KB",
    uploadedAt: "3d atrás",
  },
];

// ─── Chat ────────────────────────────────────────────────────────────────────

export const initialMessages: Message[] = [
  {
    id: "msg-001",
    role: "assistant",
    content:
      "Olá! Estou pronto para responder perguntas sobre **1.284 documentos** indexados. Posso consultar políticas, contratos, manuais e tabelas. Qual é a sua dúvida?",
    timestamp: "14:28:00",
  },
  {
    id: "msg-002",
    role: "user",
    content: "Quais são as regras de reembolso para despesas de home office?",
    timestamp: "14:29:12",
  },
  {
    id: "msg-003",
    role: "assistant",
    content:
      "Segundo a **Política de Reembolso 2024**, colaboradores em regime de home office têm direito a:\n\n• **Internet:** até R$120/mês mediante comprovante\n• **Energia elétrica:** R$80 fixo mensal, sem comprovante necessário\n• **Cadeira/ergonomia:** até R$800 por ano, com aprovação do gestor\n• **Monitor/periféricos:** até R$1.200 por ano, requer 3 orçamentos\n\nPrazo para solicitação: até 30 dias após o mês de referência. Aprovação automática para valores abaixo de R$200.",
    sources: [
      {
        document: "politica-reembolso-2024.pdf",
        page: 4,
        score: 0.96,
        excerpt: "Colaboradores em regime home office são elegíveis a reembolso de infraestrutura conforme tabela §3.2...",
      },
      {
        document: "manual-rh-v3.docx",
        section: "seção 8.2",
        score: 0.88,
        excerpt: "Solicitações de reembolso devem ser enviadas via portal RH até o dia 30 do mês seguinte...",
      },
    ],
    meta: {
      chunks: 4,
      tokens: 847,
      latency: 1.24,
      model: "gpt-4o-mini",
    },
    timestamp: "14:29:15",
  },
];

// ─── Agents ───────────────────────────────────────────────────────────────────

export const agentConfigs: AgentConfig[] = [
  {
    id: "analyst",
    name: "Document Analyst",
    description:
      "Analisa documentos para extrair pontos-chave, riscos, resumo executivo e FAQ automático.",
    capabilities: ["resumo", "extração", "riscos", "faq"],
    colorClass: "analyst",
    emoji: "📄",
  },
  {
    id: "ticket",
    name: "Ticket Assistant",
    description:
      "Analisa chamados, classifica prioridade, identifica área responsável e sugere resposta.",
    capabilities: ["classificação", "prioridade", "resposta"],
    colorClass: "ticket",
    emoji: "🎫",
  },
  {
    id: "workflow",
    name: "Workflow Planner",
    description:
      "Quebra solicitações complexas em etapas, aciona ferramentas e sugere próximas ações.",
    capabilities: ["planejamento", "etapas", "tools"],
    colorClass: "workflow",
    emoji: "⚡",
  },
];

export const mockAgentResult: AgentResult = {
  agentName: "Ticket Assistant",
  input:
    "Cliente Mariana Souza solicitou cancelamento do contrato Premium com reembolso proporcional de 47 dias não utilizados.",
  steps: [
    {
      number: 1,
      title: "Identificação da política aplicável",
      text: "Consultados 3 documentos no RAG. Política de Cancelamento §4.2 se aplica: contratos Premium com mais de 30 dias permitem reembolso proporcional.",
      tag: "RAG · score 0.94",
      tagVariant: "info",
    },
    {
      number: 2,
      title: "Validação de prazo e cálculo",
      text: "47 dias restantes identificados. Valor de reembolso calculado: R$156,33 (47/30 × R$99,90). Prazo para processamento: 5 dias úteis.",
      tag: "financeiro · calculado",
      tagVariant: "fin",
    },
    {
      number: 3,
      title: "Classificação do ticket",
      text: "Prioridade: Normal. Área responsável: CS Financeiro. SLA: 48h. Motivo: insatisfação com features (categoria: churn_voluntário).",
      tag: "prioridade normal · CS Financeiro",
      tagVariant: "warn",
    },
    {
      number: 4,
      title: "Resposta sugerida ao cliente",
      text: '"Olá Mariana, confirmamos o cancelamento do seu plano Premium. O reembolso de R$156,33 será processado em até 5 dias úteis na forma de pagamento original."',
      tag: "resposta gerada · aprovação necessária",
      tagVariant: "fin",
    },
  ],
  latency: 1.8,
  tokens: 1243,
  executedAt: "42 min atrás",
};

// ─── Logs ────────────────────────────────────────────────────────────────────

export const mockLogs: LogEntry[] = [
  {
    id: "log-001",
    timestamp: "14:32:18",
    type: "RAG",
    operation: "regras de reembolso home office",
    tokens: 847,
    latency: 1.24,
    docs: 4,
    status: "ok",
    promptSent:
      'System: Você é um assistente corporativo... Use apenas as fontes fornecidas...\nContext: [CHUNK_1: politica-reembolso-2024.pdf p.4...] [CHUNK_2: manual-rh-v3.docx §8.2...]\nUser: Quais são as regras de reembolso para despesas de home office?',
    retrievedChunks: [
      "📄 politica-reembolso-2024.pdf · chunk_047 · score 0.9612",
      "📄 politica-reembolso-2024.pdf · chunk_048 · score 0.9441",
      "📄 manual-rh-v3.docx · chunk_183 · score 0.8827",
      "📄 manual-rh-v3.docx · chunk_184 · score 0.8712",
    ],
  },
  {
    id: "log-002",
    timestamp: "14:18:44",
    type: "AGENT",
    operation: "Ticket #4821 — Ticket Assistant",
    tokens: 1243,
    latency: 1.8,
    docs: 3,
    status: "ok",
    promptSent:
      "System: Você é o Ticket Assistant. Analise o chamado e execute as etapas: 1) identifique política 2) valide prazo 3) classifique 4) gere resposta...\nUser: \"Cliente Mariana Souza solicitou cancelamento...\"",
    toolsCalled: [
      '🔧 rag_search("política cancelamento premium") → 3 docs',
      "🔧 calculate_refund(days=47, plan=\"premium\") → R$156.33",
      '🔧 classify_ticket(type="cancellation") → "CS Financeiro / Normal"',
    ],
  },
  {
    id: "log-003",
    timestamp: "13:55:02",
    type: "EMBED",
    operation: "manual-rh-v3.docx — 612 chunks",
    tokens: 47200,
    latency: 12.4,
    docs: null,
    status: "ok",
    promptSent:
      'extract_text(docx) → 612 chunks via RecursiveCharacterTextSplitter(size=512, overlap=50)\ngenerate_embeddings(model="text-embedding-3-small") → 1536-dim vectors\nupsert_pgvector(table="document_chunks", count=612)',
  },
  {
    id: "log-004",
    timestamp: "13:21:37",
    type: "RAG",
    operation: "prazo para solicitação de férias",
    tokens: 612,
    latency: 0.98,
    docs: 3,
    status: "ok",
    retrievedChunks: [
      "📄 manual-rh-v3.docx · chunk_091 · score 0.9311",
      "📄 manual-rh-v3.docx · chunk_092 · score 0.9204",
      "📄 politica-ferias-2024.pdf · chunk_012 · score 0.8891",
    ],
  },
  {
    id: "log-005",
    timestamp: "12:44:19",
    type: "RAG",
    operation: "valor do plano dental corporativo",
    tokens: 523,
    latency: 3.12,
    docs: 2,
    status: "warn",
    warning:
      "pgvector timeout na 2ª query (>2s). Resultado entregue com apenas 2 dos 4 chunks esperados. Considere otimizar o índice HNSW para este namespace.",
  },
];
