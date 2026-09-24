import { useState, useRef } from "react";
import { Upload as UploadIcon, Plus, Trash2 } from "lucide-react";
import { PageHeader } from "@/components/layout/PageHeader";
import { useDocuments, useUploadDocument, useDeleteDocument } from "@/hooks/useDocuments";
import { toast } from "@/hooks/use-toast";

const formatColors: Record<string, string> = {
  pdf: "bg-red-500/15 text-red-400",
  docx: "bg-primary/10 text-primary",
  xlsx: "bg-emerald-500/15 text-emerald-400",
  txt: "bg-secondary text-foreground/70",
  md: "bg-violet-500/15 text-violet-400",
};

function ProgressBar({ pct, color }: { pct: number; color: string }) {
  return (
    <div className="h-0.5 bg-border rounded-full overflow-hidden mt-2">
      <div className={`h-full rounded-full transition-all duration-700 ${color}`} style={{ width: `${pct}%` }} />
    </div>
  );
}

export default function Upload() {
  const { data: docs = [] } = useDocuments();
  const upload = useUploadDocument();
  const remove = useDeleteDocument();
  const [isDragging, setIsDragging] = useState(false);
  const fileRef = useRef<HTMLInputElement>(null);

  async function handleFiles(files: FileList | null) {
    if (!files || files.length === 0) return;
    for (const f of Array.from(files)) {
      try {
        await upload.mutateAsync(f);
        toast({ title: "Upload iniciado", description: f.name });
      } catch (err) {
        const msg = err instanceof Error ? err.message : "Falha no upload";
        toast({ title: "Erro no upload", description: msg, variant: "destructive" });
      }
    }
  }

  async function handleDelete(id: string, name: string) {
    try {
      await remove.mutateAsync(id);
      toast({ title: "Documento removido", description: name });
    } catch (err) {
      const msg = err instanceof Error ? err.message : "Falha ao remover";
      toast({ title: "Erro ao remover", description: msg, variant: "destructive" });
    }
  }

  function handleDrop(e: React.DragEvent) {
    e.preventDefault();
    setIsDragging(false);
    handleFiles(e.dataTransfer.files);
  }

  const indexed = docs.filter((d) => d.status === "indexado");
  const totalChunks = indexed.reduce((s, d) => s + d.chunks, 0);
  const totalTokens = indexed.reduce((s, d) => s + d.tokens, 0);

  return (
    <div className="flex flex-col flex-1 overflow-auto">
      <PageHeader
        title="Upload de Documentos"
        subtitle="Indexação automática via pipeline RAG"
        actions={
          <button
            onClick={() => fileRef.current?.click()}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-primary text-primary-foreground text-xs hover:bg-primary/90 transition-all"
          >
            <Plus className="w-3 h-3" /> Novo Upload
          </button>
        }
      />

      <div className="p-6 flex-1 overflow-auto">
        <input
          ref={fileRef}
          type="file"
          multiple
          accept=".pdf,.docx,.xlsx,.txt,.md"
          className="hidden"
          onChange={(e) => handleFiles(e.target.files)}
        />
        <div
          onClick={() => fileRef.current?.click()}
          onDragOver={(e) => { e.preventDefault(); setIsDragging(true); }}
          onDragLeave={() => setIsDragging(false)}
          onDrop={handleDrop}
          className={`border-2 border-dashed rounded-xl p-12 text-center cursor-pointer transition-all mb-6 ${
            isDragging ? "border-primary bg-primary/5" : "border-border hover:border-primary/50 hover:bg-primary/5"
          }`}
        >
          <div className="w-12 h-12 bg-primary/10 rounded-xl flex items-center justify-center mx-auto mb-4">
            <UploadIcon className="w-6 h-6 text-primary" />
          </div>
          <div className="text-sm font-semibold mb-1.5">
            {upload.isPending ? "Enviando..." : "Arraste arquivos ou clique para selecionar"}
          </div>
          <div className="text-xs text-muted-foreground mb-4">Máximo 50MB por arquivo · TXT/MD funcionam end-to-end no MVP</div>
          <div className="flex items-center justify-center gap-2 flex-wrap">
            {["PDF", "DOCX", "XLSX", "TXT", "MD"].map((f) => (
              <span key={f} className="text-[11px] px-2.5 py-1 rounded-full border border-border text-muted-foreground font-mono">
                {f}
              </span>
            ))}
          </div>
        </div>

        <div className="font-mono text-[10px] text-muted-foreground uppercase tracking-widest mb-3">Documentos</div>
        <div className="flex flex-col gap-3 mb-6">
          {docs.length === 0 && (
            <div className="text-xs text-muted-foreground py-4">Nenhum documento ainda.</div>
          )}
          {docs.map((doc) => {
            const isProcessing = doc.status === "processando";
            const isQueued = doc.status === "na_fila";
            const isDone = doc.status === "indexado";
            const isError = doc.status === "erro";
            const pct = isDone ? 100 : isProcessing ? 60 : isError ? 100 : 12;

            return (
              <div key={doc.id} className="bg-card border border-border rounded-xl p-4 flex items-center gap-4">
                <div className={`w-9 h-9 rounded-lg flex items-center justify-center text-[11px] font-bold flex-shrink-0 ${formatColors[doc.type] ?? formatColors.txt}`}>
                  {doc.type.toUpperCase().slice(0, 3)}
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between gap-2">
                    <span className="text-xs font-medium truncate">{doc.name}</span>
                    {isDone && <span className="text-[11px] text-emerald-400 flex-shrink-0">✓ Indexado</span>}
                    {isProcessing && <span className="text-[11px] text-primary font-mono flex-shrink-0">⟳ Gerando embeddings…</span>}
                    {isQueued && <span className="text-[11px] text-muted-foreground flex-shrink-0">⟳ Aguardando…</span>}
                    {isError && (
                      <div className="flex items-center gap-2 flex-shrink-0">
                        <span className="text-[11px] text-red-400">✗ Erro</span>
                        <button
                          onClick={() => handleDelete(doc.id, doc.name)}
                          disabled={remove.isPending}
                          className="p-1 rounded hover:bg-red-500/10 text-red-400 hover:text-red-300 transition-colors disabled:opacity-50"
                          title="Remover documento"
                        >
                          <Trash2 className="w-3 h-3" />
                        </button>
                      </div>
                    )}
                  </div>
                  <div className="text-[11px] text-muted-foreground mt-0.5">
                    {isDone ? `${doc.chunks} chunks · ${(doc.tokens / 1000).toFixed(1)}K tokens` :
                     isProcessing ? "processando…" :
                     isError ? (doc.processingError ?? "falha no processamento") :
                     "extração pendente"} · {doc.size} · {doc.uploadedAt}
                  </div>
                  <ProgressBar
                    pct={pct}
                    color={isDone ? "bg-emerald-500" : isError ? "bg-red-500" : isProcessing ? "bg-gradient-to-r from-blue-500 to-cyan-400" : "bg-muted-foreground"}
                  />
                </div>
              </div>
            );
          })}
        </div>

        <div className="grid grid-cols-3 gap-3">
          {[
            { val: String(indexed.length), label: "documentos indexados", color: "text-primary" },
            { val: totalChunks >= 1000 ? `${(totalChunks / 1000).toFixed(1)}K` : String(totalChunks), label: "chunks no pgvector", color: "text-cyan-400" },
            { val: totalTokens >= 1000 ? `${(totalTokens / 1000).toFixed(1)}K` : String(totalTokens), label: "tokens embedados", color: "text-emerald-400" },
          ].map((s) => (
            <div key={s.label} className="bg-card border border-border rounded-xl p-4 text-center">
              <div className={`font-mono text-xl font-bold ${s.color}`}>{s.val}</div>
              <div className="text-[11px] text-muted-foreground mt-1">{s.label}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
