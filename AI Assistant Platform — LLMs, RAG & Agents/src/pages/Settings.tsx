import { useState } from "react";
import { Eye, EyeOff, Save, Key, AppWindow } from "lucide-react";
import { PageHeader } from "@/components/layout/PageHeader";
import { toast } from "@/hooks/use-toast";
import { getSettings, saveSettings } from "@/hooks/useSettings";

function Field({ label, value, onChange, mono = false }: {
  label: string;
  value: string;
  onChange: (v: string) => void;
  mono?: boolean;
}) {
  return (
    <div className="flex flex-col gap-1.5">
      <label className="text-xs text-muted-foreground">{label}</label>
      <input
        type="text"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className={`bg-background border border-border rounded-lg px-3 py-2 text-sm focus:outline-none focus:border-primary transition-colors ${mono ? "font-mono" : ""}`}
      />
    </div>
  );
}

export default function SettingsPage() {
  const [cfg, setCfg] = useState(() => getSettings());
  const [showKey, setShowKey] = useState(false);

  function set(key: keyof typeof cfg) {
    return (v: string) => setCfg((prev) => ({ ...prev, [key]: v }));
  }

  function handleSave() {
    saveSettings({ ...cfg, openaiApiKey: cfg.openaiApiKey.trim() });
    toast({ title: "Configurações salvas" });
  }

  const masked = cfg.openaiApiKey
    ? `${cfg.openaiApiKey.slice(0, 7)}${"•".repeat(Math.max(0, cfg.openaiApiKey.length - 11))}${cfg.openaiApiKey.slice(-4)}`
    : "";

  return (
    <div className="flex flex-col flex-1 overflow-auto">
      <PageHeader title="Configurações" subtitle="Chaves de API e identidade da plataforma" />

      <div className="p-6 max-w-xl flex flex-col gap-6">

        {/* App identity */}
        <div className="bg-card border border-border rounded-xl p-5 flex flex-col gap-4">
          <div className="flex items-center gap-2">
            <AppWindow className="w-4 h-4 text-primary" />
            <span className="text-sm font-semibold">Identidade da Aplicação</span>
          </div>
          <Field label="Nome" value={cfg.appName} onChange={set("appName")} />
          <Field label="Tagline" value={cfg.appTagline} onChange={set("appTagline")} />
          <div className="grid grid-cols-2 gap-3">
            <Field label="Versão" value={cfg.appVersion} onChange={set("appVersion")} mono />
            <Field label="Canal" value={cfg.appChannel} onChange={set("appChannel")} mono />
          </div>
        </div>

        {/* OpenAI API Key */}
        <div className="bg-card border border-border rounded-xl p-5 flex flex-col gap-4">
          <div className="flex items-center gap-2">
            <Key className="w-4 h-4 text-primary" />
            <span className="text-sm font-semibold">OpenAI API Key</span>
          </div>
          <p className="text-xs text-muted-foreground">
            Necessária para geração de embeddings e respostas do Chat RAG. A chave é armazenada localmente no seu
            navegador e enviada apenas para as Edge Functions do Supabase.
          </p>
          <div className="relative">
            <input
              type={showKey ? "text" : "password"}
              value={cfg.openaiApiKey}
              onChange={(e) => setCfg((prev) => ({ ...prev, openaiApiKey: e.target.value }))}
              placeholder="sk-..."
              className="w-full bg-background border border-border rounded-lg px-3 py-2 text-sm pr-10 font-mono focus:outline-none focus:border-primary transition-colors"
            />
            <button
              type="button"
              onClick={() => setShowKey((v) => !v)}
              className="absolute right-2.5 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground transition-colors"
            >
              {showKey ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
            </button>
          </div>
          {cfg.openaiApiKey && !showKey && (
            <p className="text-[11px] text-muted-foreground font-mono">{masked}</p>
          )}
        </div>

        <div className="bg-amber-500/5 border border-amber-500/20 rounded-xl p-4">
          <p className="text-xs text-amber-400/80">
            <strong className="text-amber-400">Alternativa:</strong> configure{" "}
            <code className="font-mono bg-amber-500/10 px-1 rounded">OPENAI_API_KEY</code> como secret nas Edge
            Functions do Supabase Dashboard para não precisar inserir a chave aqui.
          </p>
        </div>

        <button
          onClick={handleSave}
          className="flex items-center gap-2 px-4 py-2 rounded-lg bg-primary text-primary-foreground text-sm hover:bg-primary/90 transition-all self-start"
        >
          <Save className="w-3.5 h-3.5" />
          Salvar configurações
        </button>
      </div>
    </div>
  );
}
