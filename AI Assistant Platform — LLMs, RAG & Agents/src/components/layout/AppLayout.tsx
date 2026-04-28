import { Outlet, useLocation, useNavigate } from "react-router-dom";
import { LayoutDashboard, Upload, MessageSquare, Bot, ScrollText, Sparkles, LogOut, Settings } from "lucide-react";
import { cn } from "@/lib/utils";
import { useAuth } from "@/hooks/useAuth";
import { getSettings } from "@/hooks/useSettings";

const navItems = [
  { label: "Dashboard", icon: LayoutDashboard, path: "/dashboard", section: "Principal" },
  { label: "Upload", icon: Upload, path: "/upload", badge: "3", section: null },
  { label: "Chat RAG", icon: MessageSquare, path: "/chat", section: null },
  { label: "Agentes IA", icon: Bot, path: "/agents", badge: "3", section: "Agentes" },
  { label: "Logs & Obs.", icon: ScrollText, path: "/logs", section: "Sistema" },
  { label: "Configurações", icon: Settings, path: "/settings", section: null },
];

export function AppLayout() {
  const location = useLocation();
  const navigate = useNavigate();
  const { user, signOut } = useAuth();
  const cfg = getSettings();
  const appFullName = `${cfg.appName} — ${cfg.appTagline}`;
  const appVersionLabel = `v${cfg.appVersion} ${cfg.appChannel}`;
  const email = user?.email ?? "";
  const initials = email ? email.slice(0, 2).toUpperCase() : "??";
  const handleSignOut = async () => {
    await signOut();
    navigate("/auth", { replace: true });
  };

  return (
    <div className="flex h-screen bg-background text-foreground font-sans overflow-hidden">
      {/* Sidebar */}
      <aside className="w-[220px] min-w-[220px] bg-card border-r border-border flex flex-col">
        {/* Logo */}
        <div className="px-4 py-5 border-b border-border flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-blue-500 to-cyan-400 flex items-center justify-center flex-shrink-0">
            <Sparkles className="w-4 h-4 text-white" />
          </div>
          <div>
            <div className="font-mono text-[11px] font-bold tracking-wide leading-tight">{appFullName}</div>
            <div className="font-mono text-[10px] text-muted-foreground">{appVersionLabel}</div>
          </div>
        </div>

        {/* Nav */}
        <nav className="flex-1 px-2 py-3">
          {navItems.map((item, i) => {
            const isActive = location.pathname === item.path;
            const showSection =
              item.section &&
              (i === 0 || navItems[i - 1].section !== item.section);

            return (
              <div key={item.path}>
                {showSection && (
                  <div className="font-mono text-[10px] text-muted-foreground uppercase tracking-widest px-2 pt-3 pb-1">
                    {item.section}
                  </div>
                )}
                <button
                  onClick={() => navigate(item.path)}
                  className={cn(
                    "w-full flex items-center gap-2.5 px-2.5 py-2 rounded-lg text-sm mb-0.5 transition-all",
                    isActive
                      ? "bg-primary/10 text-primary border border-primary/25"
                      : "text-foreground/70 hover:bg-secondary hover:text-foreground border border-transparent"
                  )}
                >
                  <item.icon className={cn("w-4 h-4 flex-shrink-0", isActive ? "opacity-100" : "opacity-70")} />
                  <span>{item.label}</span>
                  {item.badge && (
                    <span className="ml-auto bg-primary/15 text-primary text-[10px] px-1.5 py-0.5 rounded-full font-mono">
                      {item.badge}
                    </span>
                  )}
                </button>
              </div>
            );
          })}
        </nav>

        {/* User */}
        <div className="p-3 border-t border-border">
          <div className="flex items-center gap-2 p-2 rounded-lg bg-secondary cursor-pointer hover:bg-muted transition-colors">
            <div className="w-7 h-7 rounded-full bg-gradient-to-br from-indigo-500 to-purple-500 flex items-center justify-center text-[11px] font-bold flex-shrink-0">
              {initials}
            </div>
            <div className="flex-1 min-w-0">
              <div className="text-xs font-medium truncate">{email || "Usuário"}</div>
              <div className="text-[11px] text-muted-foreground">Autenticado</div>
            </div>
            <button
              onClick={handleSignOut}
              title="Sair"
              className="p-1.5 rounded-md text-foreground/70 hover:text-foreground hover:bg-muted transition-colors flex-shrink-0"
            >
              <LogOut className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      </aside>

      {/* Content */}
      <main className="flex-1 flex flex-col overflow-hidden">
        <Outlet />
      </main>
    </div>
  );
}
