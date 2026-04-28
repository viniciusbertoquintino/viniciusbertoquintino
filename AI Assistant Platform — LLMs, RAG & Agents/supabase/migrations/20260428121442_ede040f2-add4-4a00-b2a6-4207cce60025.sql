
-- pgvector
create extension if not exists vector;

-- ============ documents ============
create table public.documents (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  type text not null,
  status text not null default 'na_fila',
  size_bytes bigint default 0,
  chunks_count int default 0,
  tokens_count int default 0,
  avg_score float default 0,
  processing_error text,
  processing_time_ms int,
  content_hash text,
  storage_path text,
  created_at timestamptz not null default now()
);
create index idx_documents_hash on public.documents(content_hash);
create index idx_documents_created on public.documents(created_at desc);

-- ============ document_chunks ============
create table public.document_chunks (
  id uuid primary key default gen_random_uuid(),
  document_id uuid not null references public.documents(id) on delete cascade,
  chunk_index int not null,
  content text not null,
  embedding vector(1536),
  tokens int default 0,
  created_at timestamptz not null default now()
);
create index idx_chunks_document on public.document_chunks(document_id);
create index idx_chunks_embedding on public.document_chunks
  using hnsw (embedding vector_cosine_ops);

-- ============ chat_sessions ============
create table public.chat_sessions (
  id uuid primary key default gen_random_uuid(),
  title text default 'Nova conversa',
  created_at timestamptz not null default now()
);

-- ============ chat_messages ============
create table public.chat_messages (
  id uuid primary key default gen_random_uuid(),
  session_id uuid not null references public.chat_sessions(id) on delete cascade,
  role text not null check (role in ('user','assistant','system')),
  content text not null,
  sources jsonb,
  prompt text,
  tokens_used int default 0,
  latency_ms int default 0,
  cost_estimate float default 0,
  model text,
  eval_score float,
  created_at timestamptz not null default now()
);
create index idx_messages_session on public.chat_messages(session_id, created_at);
create index idx_messages_created on public.chat_messages(created_at desc);

-- ============ agent_executions ============
create table public.agent_executions (
  id uuid primary key default gen_random_uuid(),
  agent_type text not null check (agent_type in ('analyst','ticket','workflow')),
  input_text text not null,
  output_json jsonb,
  reasoning jsonb,
  tools_used jsonb,
  confidence float,
  tokens_used int default 0,
  latency_ms int default 0,
  cost_estimate float default 0,
  model text,
  status text default 'done',
  created_at timestamptz not null default now()
);
create index idx_agents_created on public.agent_executions(created_at desc);

-- ============ RLS (MVP permissivo — sem autenticação ainda) ============
alter table public.documents enable row level security;
alter table public.document_chunks enable row level security;
alter table public.chat_sessions enable row level security;
alter table public.chat_messages enable row level security;
alter table public.agent_executions enable row level security;

create policy "mvp_open_documents" on public.documents
  for all to anon, authenticated using (true) with check (true);
create policy "mvp_open_chunks" on public.document_chunks
  for all to anon, authenticated using (true) with check (true);
create policy "mvp_open_sessions" on public.chat_sessions
  for all to anon, authenticated using (true) with check (true);
create policy "mvp_open_messages" on public.chat_messages
  for all to anon, authenticated using (true) with check (true);
create policy "mvp_open_agents" on public.agent_executions
  for all to anon, authenticated using (true) with check (true);

-- ============ RPC: busca semântica ============
create or replace function public.match_document_chunks(
  query_embedding vector(1536),
  match_threshold float default 0.7,
  match_count int default 4
)
returns table (
  chunk_id uuid,
  document_id uuid,
  document_name text,
  chunk_index int,
  content text,
  score float
)
language sql
stable
security definer
set search_path = public
as $$
  select
    dc.id as chunk_id,
    dc.document_id,
    d.name as document_name,
    dc.chunk_index,
    dc.content,
    1 - (dc.embedding <=> query_embedding) as score
  from public.document_chunks dc
  join public.documents d on d.id = dc.document_id
  where dc.embedding is not null
    and 1 - (dc.embedding <=> query_embedding) >= match_threshold
  order by dc.embedding <=> query_embedding
  limit match_count;
$$;

-- ============ Storage bucket ============
insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values (
  'documents',
  'documents',
  true,
  52428800,
  array['application/pdf','application/vnd.openxmlformats-officedocument.wordprocessingml.document','application/vnd.openxmlformats-officedocument.spreadsheetml.sheet','text/plain','text/markdown']
)
on conflict (id) do update set
  public = excluded.public,
  file_size_limit = excluded.file_size_limit,
  allowed_mime_types = excluded.allowed_mime_types;

create policy "mvp_documents_read" on storage.objects
  for select to anon, authenticated
  using (bucket_id = 'documents');

create policy "mvp_documents_insert" on storage.objects
  for insert to anon, authenticated
  with check (bucket_id = 'documents');

create policy "mvp_documents_update" on storage.objects
  for update to anon, authenticated
  using (bucket_id = 'documents');

create policy "mvp_documents_delete" on storage.objects
  for delete to anon, authenticated
  using (bucket_id = 'documents');
