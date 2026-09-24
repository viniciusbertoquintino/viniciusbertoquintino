import { useNavigate } from "react-router-dom";
import { RefreshCw, Plus, FileText, MessageSquare, Clock, Activity } from "lucide-react";
import { PageHeader } from "@/components/layout/PageHeader";
import { useDashboardMetrics, useRecentActivity } from "@/hooks/useDashboardMetrics";
import { useDocuments } from "@/hooks/useDocuments";
import { useQueryClient } from "@tanstack/react-query";

const resources = [
  { label: "Embeddings", pct: 71, color: "from-blue-500 to-cyan-400" },
  { label: "pgvector", pct: 38, color: "from-cyan-400 to-teal-400" },
  { label: "LLM calls", pct: 54, color: "from-violet-500 to-purple-400" },
  { label: "Storage", pct: 22, color: "from-emerald-500 to-green-400" },
];

function formatTokens(n: number) {
  if (n >= 1000) return (n / 1000).toFixed(0) + "K";
  return String(n);
}

const docTypeColors: Record<string, string> = {
  pdf: "bg-red-500/15 text-red-400",
  docx: "bg-primary/10 text-primary",
  xlsx: "bg-emerald-500/15 text-emerald-400",
  txt: "bg-secondary text-foreground/70",
  md: "bg-violet-500/15 text-violet-400",
};

export default function Dashboard() {
  const navigate = useNavigate();
  const qc = useQueryClient();
  const { data: metrics } = useDashboardMetrics();
  const { data: activity = [] } = useRecentActivity();
  const { data: documents = [] } = useDocuments();

  const m = metrics ?? { documentsIndexed: 0, ragQueries: 0, tokensToday: 0, avgLatency: 0, estimatedCost: 0, successRate: 100 };

  return (
    <div className="flex flex-col flex-1 overflow-auto">
      <PageHeader
        title="Dashboard"
        subtitle="Visão geral da plataforma"
        actions={
          <>
            <button
              onClick={() => {
                qc.invalidateQueries({ queryKey: ["dashboard-metrics"] });
                qc.invalidateQueries({ queryKey: ["recent-activity"] });
                qc.invalidateQueries({ queryKey: ["documents"] });
              }}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-border bg-secondary text-foreground/70 text-xs hover:border-primary hover:text-primary transition-all"
            >
              <RefreshCw className="w-3 h-3" /> Atualizar
            </button>
            <button
              onClick={() => navigate("/upload")}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-primary text-primary-foreground text-xs hover:bg-primary/90 transition-all"
            >
              <Plus className="w-3 h-3" /> Upload
            </button>
          </>
        }
      />

      <div className="p-6 flex-1 overflow-auto">
        {/* Metrics */}
        <div className="grid grid-cols-4 gap-4 mb-6">
          {[
            { icon: FileText, label: "Documentos", value: m.documentsIndexed.toLocaleString("pt-BR"), delta: "indexados", color: "text-primary" },
            { icon: MessageSquare, label: "Consultas RAG", value: m.ragQueries.toLocaleString("pt-BR"), delta: "totais", color: "text-cyan-400" },
            { icon: Clock, label: "Tokens hoje", value: formatTokens(m.tokensToday), delta: `custo ~$${m.estimatedCost.toFixed(4)}`, color: "text-violet-400" },
            { icon: Activity, label: "Latência média", value: `${m.avgLatency}s`, delta: "respostas hoje", color: "text-emerald-400" },
          ].map((mItem) => (
            <div key={mItem.label} className="bg-card border border-border rounded-xl p-4">
              <div className="flex items-center gap-1.5 font-mono text-[10px] text-muted-foreground uppercase tracking-wider mb-2">
                <mItem.icon className="w-3 h-3" />
                {mItem.label}
              </div>
              <div className={`font-mono text-3xl font-bold tracking-tight mb-1 ${mItem.color}`}>{mItem.value}</div>
              <div className="text-[11px] text-emerald-400">{mItem.delta}</div>
            </div>
          ))}
        </div>

        <div className="grid grid-cols-2 gap-4 mb-4">
          {/* Recent docs */}
          <div className="bg-card border border-border rounded-xl p-5">
            <div className="flex items-center justify-between mb-4">
              <span className="font-mono text-xs font-semibold text-foreground">Documentos recentes</span>
              <span className="text-[10px] text-muted-foreground">últimos 4</span>
            </div>
            {documents.length === 0 && (
              <div className="text-xs text-muted-foreground py-4">Nenhum documento ainda. Faça upload na aba Upload.</div>
            )}
            {documents.slice(0, 4).map((doc) => (
              <div key={doc.id} className="flex items-center gap-3 py-2.5 border-b border-border last:border-0 last:pb-0">
                <div className={`w-8 h-8 rounded-md flex items-center justify-center text-[11px] font-bold flex-shrink-0 ${docTypeColors[doc.type] ?? docTypeColors.txt}`}>
                  {doc.type.toUpperCase().slice(0, 3)}
                </div>
                <div className="flex-1 min-w-0">
                  <div className="text-xs font-medium truncate text-foreground">{doc.name}</div>
                  <div className="text-[11px] text-muted-foreground mt-0.5">
                    {doc.status === "indexado" ? `${doc.chunks} chunks · ${(doc.tokens / 1000).toFixed(1)}K tokens` : "processando..."} · {doc.uploadedAt}
                  </div>
                </div>
                {doc.status === "indexado" ? (
                  <span className="text-[10px] px-2 py-0.5 rounded-full bg-emerald-500/15 text-emerald-400 font-mono flex-shrink-0">✓ indexado</span>
                ) : doc.status === "processando" ? (
                  <span className="text-[10px] px-2 py-0.5 rounded-full bg-amber-500/15 text-amber-400 font-mono flex-shrink-0">⟳ processando</span>
                ) : (
                  <span className="text-[10px] px-2 py-0.5 rounded-full bg-secondary text-muted-foreground font-mono flex-shrink-0">na fila</span>
                )}
              </div>
            ))}
          </div>

          {/* Activity */}
          <div className="bg-card border border-border rounded-xl p-5">
            <div className="font-mono text-xs font-semibold text-foreground mb-4">Atividade recente</div>
            {activity.length === 0 && <div className="text-xs text-muted-foreground py-4">Sem atividade ainda.</div>}
            {activity.map((a) => (
              <div key={a.id} className="flex gap-3 py-2 border-b border-border last:border-0 text-xs">
                <div className="w-1.5 h-1.5 rounded-full mt-1.5 flex-shrink-0" style={{ background: a.color }} />
                <div>
                  <div className="text-foreground/70 leading-relaxed">{a.text}</div>
                  <div className="text-muted-foreground text-[11px] mt-0.5">{a.time}</div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Resource usage */}
        <div className="bg-card border border-border rounded-xl p-5">
          <div className="flex items-center justify-between mb-4">
            <span className="font-mono text-xs font-semibold text-foreground">Uso de recursos</span>
            <span className="text-[10px] text-muted-foreground">hoje vs capacidade</span>
          </div>
          <div className="grid grid-cols-4 gap-5">
            {resources.map((r) => (
              <div key={r.label}>
                <div className="flex justify-between text-[11px] mb-1.5">
                  <span className="text-muted-foreground">{r.label}</span>
                  <span className="text-primary font-mono">{r.pct}%</span>
                </div>
                <div className="h-1 bg-border rounded-full overflow-hidden">
                  <div className={`h-full bg-gradient-to-r ${r.color} rounded-full transition-all`} style={{ width: `${r.pct}%` }} />
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
