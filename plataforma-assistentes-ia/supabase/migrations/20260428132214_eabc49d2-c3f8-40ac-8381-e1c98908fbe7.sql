-- Drop open policies and replace with authenticated-only policies

DROP POLICY IF EXISTS mvp_open_documents ON public.documents;
DROP POLICY IF EXISTS mvp_open_chunks ON public.document_chunks;
DROP POLICY IF EXISTS mvp_open_sessions ON public.chat_sessions;
DROP POLICY IF EXISTS mvp_open_messages ON public.chat_messages;
DROP POLICY IF EXISTS mvp_open_agents ON public.agent_executions;

CREATE POLICY auth_all_documents ON public.documents
  FOR ALL TO authenticated
  USING (auth.uid() IS NOT NULL)
  WITH CHECK (auth.uid() IS NOT NULL);

CREATE POLICY auth_all_chunks ON public.document_chunks
  FOR ALL TO authenticated
  USING (auth.uid() IS NOT NULL)
  WITH CHECK (auth.uid() IS NOT NULL);

CREATE POLICY auth_all_sessions ON public.chat_sessions
  FOR ALL TO authenticated
  USING (auth.uid() IS NOT NULL)
  WITH CHECK (auth.uid() IS NOT NULL);

CREATE POLICY auth_all_messages ON public.chat_messages
  FOR ALL TO authenticated
  USING (auth.uid() IS NOT NULL)
  WITH CHECK (auth.uid() IS NOT NULL);

CREATE POLICY auth_all_agents ON public.agent_executions
  FOR ALL TO authenticated
  USING (auth.uid() IS NOT NULL)
  WITH CHECK (auth.uid() IS NOT NULL);

-- Storage: require authenticated for documents bucket
DROP POLICY IF EXISTS "documents_public_read" ON storage.objects;
DROP POLICY IF EXISTS "documents_public_insert" ON storage.objects;
DROP POLICY IF EXISTS "documents_public_update" ON storage.objects;
DROP POLICY IF EXISTS "documents_public_delete" ON storage.objects;

CREATE POLICY "documents_auth_read" ON storage.objects
  FOR SELECT TO authenticated
  USING (bucket_id = 'documents');

CREATE POLICY "documents_auth_insert" ON storage.objects
  FOR INSERT TO authenticated
  WITH CHECK (bucket_id = 'documents');

CREATE POLICY "documents_auth_update" ON storage.objects
  FOR UPDATE TO authenticated
  USING (bucket_id = 'documents');

CREATE POLICY "documents_auth_delete" ON storage.objects
  FOR DELETE TO authenticated
  USING (bucket_id = 'documents');