import { useState } from "react";
import { PageHeader } from "@/components/layout/PageHeader";
import { agentConfigs } from "@/lib/mockData";
import { useRunAgent } from "@/hooks/useAgents";
import { toast } from "@/hooks/use-toast";
import type { AgentType, AgentResult, AgentStatus } from "@/types";

const tagStyles: Record<string, string> = {
  fin: "bg-emerald-500/15 text-emerald-400",
  risk: "bg-red-500/15 text-red-400",
  info: "bg-primary/10 text-primary",
  warn: "bg-amber-500/15 text-amber-400",
};

const accentColors: Record<AgentType, string> = {
  analyst: "from-blue-500 to-cyan-400",
  ticket: "from-violet-500 to-pink-500",
  workflow: "from-amber-500 to-red-500",
};

const PLACEHOLDERS: Record<AgentType, string> = {
  analyst: "Cole um trecho de documento para analisar (resumo, riscos, FAQ)…",
  ticket: "Descreva o ticket do cliente (ex: cancelamento, reembolso, dúvida)…",
  workflow: "Descreva a solicitação a planejar em etapas executáveis…",
};

export default function Agents() {
  const [statuses, setStatuses] = useState<Record<AgentType, AgentStatus>>({
    analyst: "ready",
    ticket: "ready",
    workflow: "ready",
  });
  const [inputs, setInputs] = useState<Record<AgentType, string>>({
    analyst: "",
    ticket: "",
    workflow: "",
  });
  const [result, setResult] = useState<AgentResult | null>(null);
  const runAgentMutation = useRunAgent();

  async function runAgent(id: AgentType) {
    const input = inputs[id].trim();
    if (!input) {
      toast({ title: "Input necessário", description: "Digite o conteúdo para o agente processar.", variant: "destructive" });
      return;
    }
    if (statuses[id] === "running") return;
    setStatuses((prev) => ({ ...prev, [id]: "running" }));
    try {
      const res = await runAgentMutation.mutateAsync({ agent_type: id, input_text: input });
      setStatuses((prev) => ({ ...prev, [id]: "done" }));
      setResult({ ...res, input });
    } catch (err) {
      const msg = err instanceof Error ? err.message : "Falha no agente";
      toast({ title: "Erro", description: msg, variant: "destructive" });
      setStatuses((prev) => ({ ...prev, [id]: "ready" }));
    }
  }

  return (
    <div className="flex flex-col flex-1 overflow-auto">
      <PageHeader
        title="Agentes Inteligentes"
        subtitle="Automação com LLMs e ferramentas"
        actions={
          <button className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-border bg-secondary text-foreground/70 text-xs hover:border-primary hover:text-primary transition-all">
            Ver execuções
          </button>
        }
      />

      <div className="p-6 flex-1 overflow-auto">
        {/* Agent cards */}
        <div className="grid grid-cols-3 gap-4 mb-6">
          {agentConfigs.map((agent) => {
            const status = statuses[agent.id];
            const isRunning = status === "running";

            return (
              <div
                key={agent.id}
                className={`bg-card border rounded-xl p-5 relative overflow-hidden transition-all ${
                  isRunning ? "border-primary/50 bg-primary/5" : "border-border hover:border-primary/40"
                }`}
              >
                <div className={`absolute top-0 left-0 right-0 h-0.5 bg-gradient-to-r ${accentColors[agent.id]}`} />

                <div className={`w-10 h-10 rounded-xl flex items-center justify-center mb-3.5 text-lg ${
                  agent.id === "analyst" ? "bg-primary/10" :
                  agent.id === "ticket" ? "bg-violet-500/15" :
                  "bg-amber-500/15"
                }`}>
                  {agent.emoji}
                </div>
                <div className="font-mono text-sm font-semibold mb-2">{agent.name}</div>
                <div className="text-xs text-foreground/70 leading-relaxed mb-3">{agent.description}</div>
                <div className="flex flex-wrap gap-1.5 mb-3">
                  {agent.capabilities.map((cap) => (
                    <span key={cap} className="text-[10px] px-2 py-0.5 rounded-full border border-border text-muted-foreground font-mono bg-secondary">
                      {cap}
                    </span>
                  ))}
                </div>

                <textarea
                  value={inputs[agent.id]}
                  onChange={(e) => setInputs((prev) => ({ ...prev, [agent.id]: e.target.value }))}
                  placeholder={PLACEHOLDERS[agent.id]}
                  rows={3}
                  className="w-full bg-secondary border border-border rounded-lg px-2.5 py-2 text-[11px] text-foreground placeholder:text-muted-foreground resize-none outline-none focus:border-primary transition-colors mb-3"
                />

                <button
                  onClick={() => runAgent(agent.id)}
                  disabled={isRunning || !inputs[agent.id].trim()}
                  className="w-full px-3 py-1.5 rounded-lg bg-primary text-primary-foreground text-xs hover:bg-primary/90 disabled:opacity-40 disabled:cursor-not-allowed transition-all mb-2"
                >
                  {isRunning ? "Executando…" : "Executar"}
                </button>

                <div className="flex items-center gap-1.5 text-[11px] text-muted-foreground">
                  <div className={`w-1.5 h-1.5 rounded-full ${
                    isRunning ? "bg-primary animate-pulse" :
                    status === "done" ? "bg-emerald-500" :
                    "bg-emerald-500"
                  }`} />
                  {isRunning ? "Executando…" : status === "done" ? "Concluído" : "Pronto"}
                </div>
              </div>
            );
          })}
        </div>

        {/* Result panel */}
        {result && (
          <div className="bg-card border border-border rounded-xl p-5">
            <div className="flex items-center gap-2.5 mb-4">
              <div className="w-3.5 h-3.5 text-primary">✓</div>
              <span className="font-mono text-xs font-semibold">Último resultado</span>
              <span className="text-[10px] px-2 py-0.5 rounded-full bg-primary/10 text-primary font-mono">{result.agentName}</span>
              <span className="ml-auto text-[11px] text-muted-foreground font-mono">
                {result.executedAt} · {result.latency}s · {(result.tokens / 1000).toFixed(1)}K tokens
              </span>
            </div>

            <div className="bg-secondary rounded-lg px-4 py-3 mb-4 text-xs text-muted-foreground border-l-2 border-primary">
              <span className="text-foreground/70">Input: </span>
              {result.input}
            </div>

            <div>
              {result.steps.map((step) => (
                <div key={step.number} className="flex gap-3 py-3 border-b border-border last:border-0 last:pb-0">
                  <div className="w-5 h-5 rounded-full bg-primary/10 text-primary font-mono text-[11px] font-bold flex items-center justify-center flex-shrink-0 mt-0.5">
                    {step.number}
                  </div>
                  <div className="flex-1">
                    <div className="text-xs font-semibold mb-1">{step.title}</div>
                    <div
                      className="text-xs text-foreground/70 leading-relaxed mb-2"
                      dangerouslySetInnerHTML={{ __html: step.text.replace(/\*\*(.*?)\*\*/g, '<strong class="text-foreground">$1</strong>') }}
                    />
                    <span className={`text-[10px] px-2 py-0.5 rounded-full font-mono ${tagStyles[step.tagVariant]}`}>
                      {step.tag}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
