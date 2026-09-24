import { useQuery } from "@tanstack/react-query";
import { supabase } from "@/integrations/supabase/client";
import { chatToLog, agentToLog, docToLog } from "@/lib/adapters";
import type { LogEntry } from "@/types";

export function useLogs() {
  return useQuery({
    queryKey: ["logs"],
    refetchInterval: 8000,
    queryFn: async (): Promise<LogEntry[]> => {
      const [chats, agents, docs] = await Promise.all([
        supabase
          .from("chat_messages")
          .select("id, content, prompt, tokens_used, latency_ms, sources, created_at, chat_sessions(title)")
          .eq("role", "assistant")
          .order("created_at", { ascending: false })
          .limit(30),
        supabase
          .from("agent_executions")
          .select("id, agent_type, input_text, reasoning, tools_used, tokens_used, latency_ms, status, created_at")
          .order("created_at", { ascending: false })
          .limit(30),
        supabase
          .from("documents")
          .select("id, name, chunks_count, tokens_count, processing_time_ms, status, processing_error, created_at")
          .in("status", ["indexado", "erro"])
          .order("created_at", { ascending: false })
          .limit(20),
      ]);

      const all: LogEntry[] = [
        ...(chats.data ?? []).map((m: any) => chatToLog(m)),
        ...(agents.data ?? []).map((a: any) => agentToLog(a)),
        ...(docs.data ?? []).map((d: any) => docToLog(d)),
      ];
      return all
        .sort((a, b) => b.timestamp.localeCompare(a.timestamp))
        .slice(0, 50);
    },
  });
}
