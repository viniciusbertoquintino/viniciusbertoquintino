import { useQuery } from "@tanstack/react-query";
import { supabase } from "@/integrations/supabase/client";

export interface DashboardMetrics {
  documentsIndexed: number;
  ragQueries: number;
  tokensToday: number;
  avgLatency: number;
  estimatedCost: number;
  successRate: number;
}

export function useDashboardMetrics() {
  return useQuery({
    queryKey: ["dashboard-metrics"],
    refetchInterval: 10000,
    queryFn: async (): Promise<DashboardMetrics> => {
      const startOfDay = new Date();
      startOfDay.setHours(0, 0, 0, 0);
      const sinceIso = startOfDay.toISOString();

      const [docsRes, msgsTodayRes, msgsAllRes] = await Promise.all([
        supabase.from("documents").select("id", { count: "exact", head: true }).eq("status", "indexado"),
        supabase
          .from("chat_messages")
          .select("tokens_used, latency_ms, cost_estimate, role")
          .gte("created_at", sinceIso),
        supabase.from("chat_messages").select("id", { count: "exact", head: true }).eq("role", "user"),
      ]);

      const today = (msgsTodayRes.data ?? []) as Array<{
        tokens_used: number | null;
        latency_ms: number | null;
        cost_estimate: number | null;
        role: string;
      }>;
      const assistantToday = today.filter((m) => m.role === "assistant");
      const tokensToday = today.reduce((s, m) => s + (m.tokens_used ?? 0), 0);
      const costToday = today.reduce((s, m) => s + (m.cost_estimate ?? 0), 0);
      const avgLatency = assistantToday.length
        ? assistantToday.reduce((s, m) => s + (m.latency_ms ?? 0), 0) / assistantToday.length / 1000
        : 0;

      return {
        documentsIndexed: docsRes.count ?? 0,
        ragQueries: msgsAllRes.count ?? 0,
        tokensToday,
        avgLatency: Number(avgLatency.toFixed(2)),
        estimatedCost: Number(costToday.toFixed(4)),
        successRate: 100,
      };
    },
  });
}

export interface ActivityItem {
  id: string;
  color: string;
  text: string;
  time: string;
}

function rel(iso: string): string {
  const m = Math.floor((Date.now() - new Date(iso).getTime()) / 60000);
  if (m < 1) return "agora";
  if (m < 60) return `há ${m} min`;
  const h = Math.floor(m / 60);
  if (h < 24) return `há ${h}h`;
  return `há ${Math.floor(h / 24)}d`;
}

export function useRecentActivity() {
  return useQuery({
    queryKey: ["recent-activity"],
    refetchInterval: 10000,
    queryFn: async (): Promise<ActivityItem[]> => {
      const [chats, agents, docs] = await Promise.all([
        supabase
          .from("chat_messages")
          .select("id, content, sources, created_at, role")
          .eq("role", "assistant")
          .order("created_at", { ascending: false })
          .limit(3),
        supabase
          .from("agent_executions")
          .select("id, agent_type, input_text, created_at")
          .order("created_at", { ascending: false })
          .limit(2),
        supabase
          .from("documents")
          .select("id, name, chunks_count, created_at, status")
          .eq("status", "indexado")
          .order("created_at", { ascending: false })
          .limit(2),
      ]);

      const items: ActivityItem[] = [];
      (chats.data ?? []).forEach((c: any) => {
        const srcCount = Array.isArray(c.sources) ? c.sources.length : 0;
        items.push({
          id: `c-${c.id}`,
          color: "#10b981",
          text: `Consulta RAG respondida — ${srcCount} fonte(s)`,
          time: rel(c.created_at),
        });
      });
      (agents.data ?? []).forEach((a: any) => {
        items.push({
          id: `a-${a.id}`,
          color: "#8b5cf6",
          text: `Agente ${a.agent_type} executado: "${a.input_text.slice(0, 60)}"`,
          time: rel(a.created_at),
        });
      });
      (docs.data ?? []).forEach((d: any) => {
        items.push({
          id: `d-${d.id}`,
          color: "#06b6d4",
          text: `Upload: ${d.name} — ${d.chunks_count ?? 0} chunks gerados`,
          time: rel(d.created_at),
        });
      });
      return items.sort((a, b) => a.time.localeCompare(b.time)).slice(0, 6);
    },
  });
}
