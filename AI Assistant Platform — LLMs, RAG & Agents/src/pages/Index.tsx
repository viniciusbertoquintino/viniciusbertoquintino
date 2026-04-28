import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Bot, FileText, MessageSquare, BarChart3, Shield, Zap, Sparkles, ArrowRight } from "lucide-react";

const features = [
  { icon: FileText, title: "Upload inteligente", desc: "PDF, Word, Excel e TXT processados automaticamente com indexação semântica." },
  { icon: MessageSquare, title: "Chat com RAG", desc: "Converse com seus documentos e receba respostas com fontes citadas." },
  { icon: Bot, title: "Agentes inteligentes", desc: "Crie agentes especializados para diferentes áreas da empresa." },
  { icon: BarChart3, title: "Métricas em tempo real", desc: "Acompanhe uso, tokens, latência e custo por interação." },
  { icon: Shield, title: "Seguro por padrão", desc: "Autenticação corporativa, RLS e logs de auditoria completos." },
  { icon: Zap, title: "Edge Functions", desc: "Processamento serverless escalável com baixa latência global." },
];

const Index = () => {
  return (
    <div className="min-h-screen bg-background">
      {/* Nav */}
      <header className="border-b border-border/60 backdrop-blur-sm bg-background/80 sticky top-0 z-50">
        <div className="container flex h-16 items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="h-8 w-8 rounded-lg flex items-center justify-center" style={{ background: 'var(--gradient-primary)' }}>
              <Sparkles className="h-4 w-4 text-primary-foreground" />
            </div>
            <span className="font-semibold tracking-tight">AI Assistant Platform</span>
          </div>
          <nav className="hidden md:flex items-center gap-8 text-sm text-muted-foreground">
            <a href="#features" className="hover:text-foreground transition">Recursos</a>
            <a href="#" className="hover:text-foreground transition">Preços</a>
            <a href="#" className="hover:text-foreground transition">Documentação</a>
          </nav>
          <div className="flex items-center gap-3">
            <Button variant="ghost" size="sm">Entrar</Button>
            <Button size="sm">Começar grátis</Button>
          </div>
        </div>
      </header>

      {/* Hero */}
      <section className="container py-24 md:py-32 text-center">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-border bg-secondary/50 text-xs font-medium text-muted-foreground mb-8">
          <span className="h-1.5 w-1.5 rounded-full bg-primary animate-pulse" />
          Nova versão com agentes inteligentes
        </div>
        <h1 className="text-5xl md:text-7xl font-bold tracking-tight max-w-4xl mx-auto leading-[1.05]">
          IA Generativa para{" "}
          <span className="bg-clip-text text-transparent" style={{ backgroundImage: 'var(--gradient-primary)' }}>
            empresas modernas
          </span>
        </h1>
        <p className="mt-6 text-lg md:text-xl text-muted-foreground max-w-2xl mx-auto">
          Centralize documentos, converse com sua base de conhecimento e automatize processos com agentes de IA — tudo em uma plataforma corporativa segura.
        </p>
        <div className="mt-10 flex items-center justify-center gap-4">
          <Button size="lg" className="gap-2">
            Acessar dashboard <ArrowRight className="h-4 w-4" />
          </Button>
          <Button size="lg" variant="outline">Ver demonstração</Button>
        </div>

        {/* Mock dashboard card */}
        <div className="mt-20 max-w-5xl mx-auto">
          <div className="rounded-2xl border border-border bg-card p-2" style={{ boxShadow: 'var(--shadow-elegant)' }}>
            <div className="rounded-xl bg-gradient-to-br from-secondary to-background p-8 md:p-12 text-left">
              <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
                {[
                  { label: "Documentos", value: "1.284" },
                  { label: "Conversas", value: "8.421" },
                  { label: "Tokens hoje", value: "412K" },
                  { label: "Latência média", value: "1.2s" },
                ].map((s) => (
                  <div key={s.label}>
                    <div className="text-xs uppercase tracking-wider text-muted-foreground">{s.label}</div>
                    <div className="text-2xl md:text-3xl font-bold mt-1">{s.value}</div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features */}
      <section id="features" className="container py-24 border-t border-border">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-bold tracking-tight">Tudo que sua equipe precisa</h2>
          <p className="mt-4 text-muted-foreground max-w-xl mx-auto">
            Uma stack completa para implementar IA generativa com governança e observabilidade.
          </p>
        </div>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((f) => (
            <Card key={f.title} className="p-6 hover:border-primary/40 transition-all hover:-translate-y-1" style={{ boxShadow: 'var(--shadow-card)' }}>
              <div className="h-10 w-10 rounded-lg bg-primary/10 flex items-center justify-center mb-4">
                <f.icon className="h-5 w-5 text-primary" />
              </div>
              <h3 className="font-semibold mb-2">{f.title}</h3>
              <p className="text-sm text-muted-foreground leading-relaxed">{f.desc}</p>
            </Card>
          ))}
        </div>
      </section>

      {/* CTA */}
      <section className="container py-24">
        <div className="rounded-2xl p-12 md:p-16 text-center text-primary-foreground" style={{ background: 'var(--gradient-primary)' }}>
          <h2 className="text-3xl md:text-4xl font-bold tracking-tight">Pronto para começar?</h2>
          <p className="mt-4 opacity-90 max-w-xl mx-auto">
            Conecte seu Supabase e configure sua chave de IA para liberar todos os recursos da plataforma.
          </p>
          <Button size="lg" variant="secondary" className="mt-8 gap-2">
            Configurar agora <ArrowRight className="h-4 w-4" />
          </Button>
        </div>
      </section>

      <footer className="border-t border-border py-8">
        <div className="container text-center text-sm text-muted-foreground">
          © 2026 AI Assistant Platform — Plataforma corporativa de IA generativa.
        </div>
      </footer>
    </div>
  );
};

export default Index;
