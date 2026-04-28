import { useNavigate } from "react-router-dom";

export default function NotFound() {
  const navigate = useNavigate();
  return (
    <div className="flex-1 flex flex-col items-center justify-center text-center p-12 bg-background">
      <div className="font-mono text-6xl font-bold text-border mb-4">404</div>
      <div className="font-mono text-sm text-muted-foreground mb-6">Página não encontrada</div>
      <button
        onClick={() => navigate("/dashboard")}
        className="px-4 py-2 rounded-lg bg-primary text-primary-foreground text-sm hover:bg-primary/90 transition-all"
      >
        Voltar ao Dashboard
      </button>
    </div>
  );
}
