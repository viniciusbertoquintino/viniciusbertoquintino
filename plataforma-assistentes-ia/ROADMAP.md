# Projeto AP — Plataforma de Assistentes com IA

**English:** Project AP — AI Assistants Platform

## Objetivo

Manter e evoluir a plataforma full-stack de LLMs, RAG e Agents (React + Supabase + backend FastAPI) com qualidade de engenharia incremental.

## Stack

- React, TypeScript, Vite, Supabase, FastAPI, Python 3.12+

## Microetapas

### Fase 0 — Base do repositório

- [x] **AP.00** Criar repositório e `.gitignore`.
  - Pronto quando: `main` possui README e primeiro commit.
- [x] **AP.01** Frontend React com páginas principais.
  - Pronto quando: Dashboard, Chat, Agents, Upload, Auth existem.
- [x] **AP.02** Supabase (migrations, edge functions, auth).
  - Pronto quando: funções RAG e agents deployáveis.
- [x] **AP.03** Backend FastAPI opcional.
  - Pronto quando: `backend/app/main.py` existe com rotas.

### Fase 1 — Alinhamento documentação

- [ ] **AP.04** Auditar README vs código real.
  - Pronto quando: README não afirma features inexistentes.
- [ ] **AP.05** Documentar setup local completo (Supabase + frontend).
  - Pronto quando: desenvolvedor consegue subir stack do zero.
- [ ] **AP.06** Validar `.env.example` cobre todas as variáveis.
  - Pronto quando: nenhum segredo necessário está faltando na doc.

### Fase 2 — Testes

- [ ] **AP.07** Expandir testes frontend (Vitest).
  - Pronto quando: componentes críticos cobertos.
- [ ] **AP.08** Adicionar testes backend (Pytest).
  - Pronto quando: rotas principais testadas.
- [ ] **AP.09** Testes para edge functions (mocks).
  - Pronto quando: chunker e RAG query testados.

### Fase 3 — Qualidade

- [ ] **AP.10** Configurar lint unificado (ESLint + Ruff).
  - Pronto quando: `npm run lint` e `ruff check` passam.
- [ ] **AP.11** Type-check estrito no frontend.
  - Pronto quando: `tsc --noEmit` passa sem erros.

### Fase 4 — Produção

- [ ] **AP.12** Docker Compose para stack local completa.
  - Pronto quando: `docker compose up` sobe frontend + backend.
- [ ] **AP.13** GitHub Actions para lint + tests.
  - Pronto quando: pipeline roda em PR.
- [ ] **AP.14** Finalizar README com métricas e limitações reais.
  - Pronto quando: documentação alinhada ao estado do código.

## Resultado que este projeto deve provar

- Plataforma RAG com embeddings e pgvector.
- Agentes especializados (Document Analyst, Ticket Assistant, Workflow Planner).
- Observabilidade (logs, tokens, latência).
- Stack full-stack deployável.
