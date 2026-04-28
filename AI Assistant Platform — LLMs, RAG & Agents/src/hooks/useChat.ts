import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { supabase } from "@/integrations/supabase/client";
import type { Message, Source } from "@/types";

function fmtTime(iso: string) {
  return new Date(iso).toLocaleTimeString("pt-BR", { hour: "2-digit", minute: "2-digit" });
}

export function useChat() {
  const [sessionId, setSessionId] = useState<string | null>(null);
  const qc = useQueryClient();

  const messagesQuery = useQuery({
    queryKey: ["chat-messages", sessionId],
    enabled: !!sessionId,
    queryFn: async (): Promise<Message[]> => {
      if (!sessionId) return [];
      const { data, error } = await supabase
        .from("chat_messages")
        .select("id, role, content, sources, tokens_used, latency_ms, model, created_at")
        .eq("session_id", sessionId)
        .order("created_at", { ascending: true });
      if (error) throw error;
      return (data ?? []).map((m: any) => ({
        id: m.id,
        role: m.role === "assistant" ? "assistant" : "user",
        content: m.content,
        sources: Array.isArray(m.sources) ? (m.sources as Source[]) : undefined,
        meta: m.role === "assistant"
          ? {
              chunks: Array.isArray(m.sources) ? m.sources.length : 0,
              tokens: m.tokens_used ?? 0,
              latency: (m.latency_ms ?? 0) / 1000,
              model: m.model ?? "gpt-4o-mini",
            }
          : undefined,
        timestamp: fmtTime(m.created_at),
      }));
    },
  });

  const sendMutation = useMutation({
    mutationFn: async (query: string) => {
      const { data, error } = await supabase.functions.invoke("rag-query", {
        body: { query, session_id: sessionId },
      });
      if (error) throw error;
      if (data?.session_id && !sessionId) setSessionId(data.session_id);
      return data;
    },
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["chat-messages", sessionId] });
    },
  });

  return {
    sessionId,
    setSessionId,
    messages: messagesQuery.data ?? [],
    isLoadingMessages: messagesQuery.isLoading,
    send: sendMutation.mutate,
    sendAsync: sendMutation.mutateAsync,
    isSending: sendMutation.isPending,
  };
}
