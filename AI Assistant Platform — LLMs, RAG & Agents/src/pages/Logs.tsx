import { useState } from "react";
import { Download } from "lucide-react";
import { PageHeader } from "@/components/layout/PageHeader";
import { useLogs } from "@/hooks/useLogs";
import type { LogType } from "@/types";

const typeColors: Record<LogType, string> = {
  RAG: "text-primary border-primary/30",
  AGENT: "text-violet-400 border-violet-500/30",
  EMBED: "text-emerald-400 border-emerald-500/30",
};

function LatencyBadge({ v }: { v: number }) {
  const cls = v < 2 ? "text-emerald-400" : v < 2.5 ? "text-amber-400" : "text-red-400";
  return <span className={`font-mono text-xs ${cls}`}>{v.toFixed(2)}s</span>;
}

export default function Logs() {
  const { data: logs = [] } = useLogs();
  const [expanded, setExpanded] = useState<string | null>(null);
  const [activeFilter, setActiveFilter] = useState("Todos");
  const [activeRange, setActiveRange] = useState("Últimas 24h");

  const types = ["Todos", "RAG", "AGENT", "EMBED"];
  const ranges = ["Últimas 24h", "7 dias", "30 dias"];

  const filtered = activeFilter === "Todos" ? logs : logs.filter((l) => l.type === activeFilter);

  function toggle(id: string) {
    setExpanded((prev) => (prev === id ? null : id));
  }

  const totalTokens = logs.reduce((s, l) => s + l.tokens, 0);
  const ragLogs = logs.filter((l) => l.type === "RAG");
  const sortedLatencies = ragLogs.map((l) => l.latency).sort((a, b) => a - b);
  const p50 = sortedLatencies[Math.floor(sortedLatencies.length * 0.5)] ?? 0;
  const p95 = sortedLatencies[Math.floor(sortedLatencies.length * 0.95)] ?? 0;

  return (
    <div className="flex flex-col flex-1 overflow-auto">
      <PageHeader
        title="Logs & Observabilidade"
        subtitle="Prompts, tokens, latência e documentos recuperados"
        actions={
          <button className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-border bg-secondary text-foreground/70 text-xs hover:border-primary hover:text-primary transition-all">
            <Download className="w-3 h-3" /> Exportar CSV
          </button>
        }
      />

      <div className="p-6 flex-1 overflow-auto">
        <div className="flex gap-2 mb-4 flex-wrap items-center">
          {types.map((t) => (
            <button
              key={t}
              onClick={() => setActiveFilter(t)}
              className={`px-3 py-1.5 rounded-full border text-xs font-mono transition-all ${
                activeFilter === t
                  ? "border-primary text-primary bg-primary/10"
                  : "border-border text-muted-foreground hover:border-primary/50 hover:text-primary"
              }`}
            >
              {t}
            </button>
          ))}
          <div className="ml-auto flex gap-2">
            {ranges.map((r) => (
              <button
                key={r}
                onClick={() => setActiveRange(r)}
                className={`px-3 py-1.5 rounded-full border text-xs font-mono transition-all ${
                  activeRange === r
                    ? "border-primary text-primary bg-primary/10"
                    : "border-border text-muted-foreground hover:border-primary/50 hover:text-primary"
                }`}
              >
                {r}
              </button>
            ))}
          </div>
        </div>

        <div className="bg-card border border-border rounded-xl overflow-hidden mb-4">
          <table className="w-full">
            <thead>
              <tr className="border-b border-border bg-card">
                {["Timestamp", "Tipo", "Query / Operação", "Tokens", "Latência", "Docs", "Status"].map((h) => (
                  <th key={h} className="text-left px-4 py-2.5 text-[10px] font-mono text-muted-foreground uppercase tracking-wider font-medium">
                    {h}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {filtered.length === 0 && (
                <tr>
                  <td colSpan={7} className="px-4 py-8 text-center text-xs text-muted-foreground">
                    Nenhum log ainda. Faça uma consulta no Chat ou execute um Agente.
                  </td>
                </tr>
              )}
              {filtered.map((log) => (
                <>
                  <tr
                    key={log.id}
                    onClick={() => toggle(log.id)}
                    className="border-b border-border last:border-0 cursor-pointer hover:bg-secondary transition-colors"
                  >
                    <td className="px-4 py-3 font-mono text-[11px] text-muted-foreground">{log.timestamp}</td>
                    <td className="px-4 py-3">
                      <span className={`font-mono text-[11px] px-2 py-0.5 rounded border ${typeColors[log.type]}`}>
                        {log.type}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-xs text-foreground/70 max-w-[200px]">
                      <div className="truncate">{log.operation}</div>
                    </td>
                    <td className="px-4 py-3 font-mono text-xs text-cyan-400">
                      {log.tokens >= 1000 ? `${(log.tokens / 1000).toFixed(1)}K` : log.tokens}
                    </td>
                    <td className="px-4 py-3"><LatencyBadge v={log.latency} /></td>
                    <td className="px-4 py-3 text-xs text-muted-foreground font-mono">{log.docs ?? "—"}</td>
                    <td className="px-4 py-3">
                      {log.status === "ok" ? (
                        <span className="text-[10px] px-2 py-0.5 rounded-full bg-emerald-500/15 text-emerald-400 font-mono">200 OK</span>
                      ) : log.status === "warn" ? (
                        <span className="text-[10px] px-2 py-0.5 rounded-full bg-amber-500/15 text-amber-400 font-mono">aviso</span>
                      ) : (
                        <span className="text-[10px] px-2 py-0.5 rounded-full bg-red-500/15 text-red-400 font-mono">erro</span>
                      )}
                    </td>
                  </tr>

                  {expanded === log.id && (
                    <tr key={`${log.id}-expanded`} className="border-b border-border last:border-0">
                      <td colSpan={7} className="px-4 pb-4 pt-0">
                        <div className="bg-secondary rounded-lg p-4 font-mono text-xs">
                          {log.promptSent && (
                            <div className="mb-3">
                              <div className="text-[10px] text-muted-foreground uppercase tracking-widest mb-2">Prompt / Reasoning</div>
                              <div className="text-foreground/70 leading-relaxed border-l-2 border-primary pl-3 whitespace-pre-wrap max-h-64 overflow-auto">{log.promptSent}</div>
                            </div>
                          )}
                          {log.retrievedChunks && log.retrievedChunks.length > 0 && (
                            <div className="mb-3">
                              <div className="text-[10px] text-muted-foreground uppercase tracking-widest mb-2">Documentos recuperados</div>
                              <div className="flex flex-col gap-1">
                                {log.retrievedChunks.map((c, i) => (
                                  <div key={i} className="text-cyan-400">{c}</div>
                                ))}
                              </div>
                            </div>
                          )}
                          {log.toolsCalled && log.toolsCalled.length > 0 && (
                            <div className="mb-3">
                              <div className="text-[10px] text-muted-foreground uppercase tracking-widest mb-2">Tools chamadas</div>
                              <div className="flex flex-col gap-1">
                                {log.toolsCalled.map((t, i) => (
                                  <div key={i} className="text-violet-400">{t}</div>
                                ))}
                              </div>
                            </div>
                          )}
                          {log.warning && (
                            <div>
                              <div className="text-[10px] text-muted-foreground uppercase tracking-widest mb-2">Aviso / Erro</div>
                              <div className="text-amber-400 border-l-2 border-amber-500 pl-3">{log.warning}</div>
                            </div>
                          )}
                        </div>
                      </td>
                    </tr>
                  )}
                </>
              ))}
            </tbody>
          </table>
        </div>

        <div className="grid grid-cols-4 gap-3">
          {[
            { val: `p50: ${p50.toFixed(2)}s`, label: "latência mediana", color: "text-primary" },
            { val: `p95: ${p95.toFixed(2)}s`, label: "latência p95", color: "text-amber-400" },
            { val: `${logs.length}`, label: "eventos totais", color: "text-emerald-400" },
            { val: totalTokens >= 1000 ? `${(totalTokens / 1000).toFixed(1)}K` : String(totalTokens), label: "tokens consumidos", color: "text-cyan-400" },
          ].map((s) => (
            <div key={s.label} className="bg-card border border-border rounded-xl p-4 text-center">
              <div className={`font-mono text-lg font-bold ${s.color}`}>{s.val}</div>
              <div className="text-[11px] text-muted-foreground mt-1">{s.label}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
