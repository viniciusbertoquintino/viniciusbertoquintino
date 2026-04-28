import { useState, useRef, useEffect } from "react";
import { Send, Plus, History } from "lucide-react";
import { PageHeader } from "@/components/layout/PageHeader";
import { useChat } from "@/hooks/useChat";
import { useDocuments } from "@/hooks/useDocuments";
import type { Message } from "@/types";

function renderContent(text: string) {
  return text
    .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
    .replace(/\n/g, "<br/>");
}

export default function Chat() {
  const { messages, send, isSending, setSessionId, sessionId } = useChat();
  const { data: documents = [] } = useDocuments();
  const [input, setInput] = useState("");
  const [dots, setDots] = useState(0);
  const msgsRef = useRef<HTMLDivElement>(null);

  // Optimistic local message (user just sent, before refetch)
  const [pendingUser, setPendingUser] = useState<Message | null>(null);
  const allMessages: Message[] = pendingUser ? [...messages, pendingUser] : messages;

  useEffect(() => {
    if (!isSending) setPendingUser(null);
  }, [isSending, messages]);

  useEffect(() => {
    if (msgsRef.current) msgsRef.current.scrollTop = msgsRef.current.scrollHeight;
  }, [allMessages, isSending]);

  useEffect(() => {
    if (!isSending) return;
    const iv = setInterval(() => setDots((d) => (d + 1) % 4), 400);
    return () => clearInterval(iv);
  }, [isSending]);

  function sendMessage() {
    const text = input.trim();
    if (!text || isSending) return;
    setInput("");
    setPendingUser({
      id: `tmp-${Date.now()}`,
      role: "user",
      content: text,
      timestamp: new Date().toLocaleTimeString("pt-BR", { hour: "2-digit", minute: "2-digit" }),
    });
    send(text);
  }

  // Active context: top-scored sources from last assistant msg
  const lastAssistant = [...messages].reverse().find((m) => m.role === "assistant");
  const contextDocs = (lastAssistant?.sources ?? []).slice(0, 5).map((s) => ({
    name: s.document,
    score: s.score,
    active: s.score >= 0.7,
  }));
  const lastMeta = lastAssistant?.meta;

  return (
    <div className="flex flex-col flex-1 overflow-hidden">
      <PageHeader
        title="Chat RAG"
        subtitle="Consulta semântica com citação de fontes"
        actions={
          <>
            <button
              onClick={() => setSessionId(null)}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-border bg-secondary text-foreground/70 text-xs hover:border-primary hover:text-primary transition-all"
            >
              <Plus className="w-3 h-3" /> Novo chat
            </button>
            <button className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-border bg-secondary text-foreground/70 text-xs hover:border-primary hover:text-primary transition-all">
              <History className="w-3 h-3" /> {sessionId ? "Sessão ativa" : "Histórico"}
            </button>
          </>
        }
      />

      <div className="flex flex-1 gap-4 p-4 overflow-hidden">
        <div className="flex-1 flex flex-col bg-card border border-border rounded-xl overflow-hidden">
          <div ref={msgsRef} className="flex-1 overflow-y-auto p-5 flex flex-col gap-4">
            {allMessages.length === 0 && !isSending && (
              <div className="text-xs text-muted-foreground text-center py-8">
                Faça uma pergunta sobre seus {documents.filter((d) => d.status === "indexado").length} documento(s) indexado(s).
              </div>
            )}
            {allMessages.map((msg) => (
              <div key={msg.id} className={`flex gap-3 items-start ${msg.role === "user" ? "flex-row-reverse" : ""}`}>
                <div className={`w-7 h-7 rounded-full flex-shrink-0 flex items-center justify-center text-[11px] font-bold ${
                  msg.role === "assistant" ? "bg-gradient-to-br from-blue-500 to-cyan-400" : "bg-gradient-to-br from-indigo-500 to-purple-500"
                }`}>
                  {msg.role === "assistant" ? "AI" : "RC"}
                </div>
                <div className={`max-w-[70%]`}>
                  <div
                    className={`px-4 py-3 rounded-xl text-xs leading-relaxed ${
                      msg.role === "assistant"
                        ? "bg-secondary border border-border rounded-tl-sm"
                        : "bg-primary/10 border border-primary/25 rounded-tr-sm text-right"
                    }`}
                    dangerouslySetInnerHTML={{ __html: renderContent(msg.content) }}
                  />
                  {msg.sources && msg.sources.length > 0 && (
                    <div className="flex flex-col gap-1 mt-2">
                      {msg.sources.map((s, i) => (
                        <div key={i} className="inline-flex items-center gap-1.5 bg-cyan-500/10 border border-cyan-500/25 rounded-md px-2.5 py-1 text-[11px] text-cyan-400 font-mono cursor-pointer hover:bg-cyan-500/20 transition-colors w-fit">
                          📄 {s.document} · score {typeof s.score === "number" ? s.score.toFixed(3) : s.score}
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            ))}

            {isSending && (
              <div className="flex gap-3 items-start">
                <div className="w-7 h-7 rounded-full flex-shrink-0 bg-gradient-to-br from-blue-500 to-cyan-400 flex items-center justify-center text-[11px] font-bold">AI</div>
                <div className="px-4 py-3 rounded-xl bg-secondary border border-border rounded-tl-sm text-xs text-muted-foreground">
                  Buscando nos documentos{".".repeat(dots + 1)}
                </div>
              </div>
            )}
          </div>

          <div className="p-4 border-t border-border flex gap-2">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); sendMessage(); }}}
              rows={1}
              placeholder="Pergunte sobre seus documentos…"
              className="flex-1 bg-secondary border border-border rounded-lg px-3 py-2 text-xs text-foreground placeholder:text-muted-foreground resize-none outline-none focus:border-primary transition-colors font-sans"
            />
            <button
              onClick={sendMessage}
              disabled={!input.trim() || isSending}
              className="px-3 py-2 rounded-lg bg-primary text-primary-foreground hover:bg-primary/90 disabled:opacity-40 disabled:cursor-not-allowed transition-all self-end"
            >
              <Send className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>

        <div className="w-60 flex flex-col gap-3 flex-shrink-0">
          <div className="bg-card border border-border rounded-xl p-4 flex-1 overflow-auto">
            <div className="font-mono text-[10px] text-muted-foreground uppercase tracking-widest mb-3">Contexto ativo</div>
            {contextDocs.length === 0 && <div className="text-[11px] text-muted-foreground">Nenhuma consulta ainda.</div>}
            {contextDocs.map((doc, i) => (
              <div key={i} className={`flex items-center gap-2 px-2 py-1.5 rounded-md mb-1 text-xs cursor-pointer transition-colors ${doc.active ? "bg-primary/10 text-primary" : "text-foreground/70 hover:bg-secondary"}`}>
                <span className="text-[11px]">📄</span>
                <span className="flex-1 truncate text-[11px]">{doc.name}</span>
                <div className="w-10 h-0.5 bg-border rounded-full overflow-hidden flex-shrink-0">
                  <div className="h-full bg-gradient-to-r from-blue-500 to-cyan-400 rounded-full" style={{ width: `${Math.max(0, Math.min(1, doc.score)) * 100}%` }} />
                </div>
                <span className={`font-mono text-[10px] flex-shrink-0 ${doc.active ? "text-primary" : "text-muted-foreground"}`}>{doc.score.toFixed(2)}</span>
              </div>
            ))}
          </div>

          <div className="bg-card border border-border rounded-xl p-4 flex-shrink-0">
            <div className="font-mono text-[10px] text-muted-foreground uppercase tracking-widest mb-3">Última query</div>
            <div className="flex flex-col gap-1.5 text-[11px]">
              {lastMeta ? (
                [
                  ["Chunks", `${lastMeta.chunks} recuperados`],
                  ["Tokens", `${lastMeta.tokens}`],
                  ["Latência", `${lastMeta.latency.toFixed(2)}s`],
                  ["Modelo", lastMeta.model],
                ].map(([label, val]) => (
                  <div key={label} className="flex gap-1">
                    <span className="text-muted-foreground flex-shrink-0">{label}:</span>
                    <span className="text-foreground/70">{val}</span>
                  </div>
                ))
              ) : (
                <div className="text-muted-foreground">—</div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
