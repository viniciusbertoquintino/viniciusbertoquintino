import { useMutation } from "@tanstack/react-query";
import { supabase } from "@/integrations/supabase/client";
import type { AgentResult, AgentType } from "@/types";

export function useRunAgent() {
  return useMutation({
    mutationFn: async ({ agent_type, input_text }: { agent_type: AgentType; input_text: string }): Promise<AgentResult> => {
      const { data, error } = await supabase.functions.invoke("run-agent", {
        body: { agent_type, input_text },
      });
      if (error) throw error;
      if (data?.error) throw new Error(data.error);
      return data as AgentResult;
    },
  });
}
