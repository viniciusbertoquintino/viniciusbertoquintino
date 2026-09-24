import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { supabase } from "@/integrations/supabase/client";
import { rowToDocument, type DocumentRow } from "@/lib/adapters";
import { getSettings } from "@/hooks/useSettings";

export function useDocuments() {
  return useQuery({
    queryKey: ["documents"],
    queryFn: async () => {
      const { data, error } = await supabase
        .from("documents")
        .select("id, name, type, status, chunks_count, tokens_count, avg_score, size_bytes, created_at, processing_error")
        .order("created_at", { ascending: false })
        .limit(50);
      if (error) throw error;
      return (data as DocumentRow[]).map(rowToDocument);
    },
    refetchInterval: (query) => {
      const docs = query.state.data ?? [];
      return docs.some((d) => d.status === "processando" || d.status === "na_fila") ? 2000 : false;
    },
  });
}

export function useDeleteDocument() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (id: string) => {
      const { data: doc } = await supabase
        .from("documents")
        .select("storage_path")
        .eq("id", id)
        .single();

      if (doc?.storage_path) {
        await supabase.storage.from("documents").remove([doc.storage_path]);
      }

      const { error } = await supabase.from("documents").delete().eq("id", id);
      if (error) throw error;
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ["documents"] }),
  });
}

export function useUploadDocument() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (file: File) => {
      const ext = (file.name.split(".").pop() ?? "txt").toLowerCase();
      const safeName = `${Date.now()}-${file.name.replace(/[^\w.\-]/g, "_")}`;
      const storagePath = safeName;

      const { error: upErr } = await supabase.storage.from("documents").upload(storagePath, file, {
        cacheControl: "3600",
        upsert: false,
      });
      if (upErr) throw upErr;

      const { data: doc, error: insErr } = await supabase
        .from("documents")
        .insert({
          name: file.name,
          type: ext,
          size_bytes: file.size,
          status: "na_fila",
          storage_path: storagePath,
        })
        .select("id")
        .single();
      if (insErr) throw insErr;

      const { openaiApiKey } = getSettings();
      const { error: fnErr } = await supabase.functions.invoke("process-document", {
        body: { document_id: doc.id, storage_path: storagePath, openai_api_key: openaiApiKey || undefined },
      });
      if (fnErr) console.error("process-document invoke error:", fnErr);

      return doc.id as string;
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ["documents"] }),
  });
}
