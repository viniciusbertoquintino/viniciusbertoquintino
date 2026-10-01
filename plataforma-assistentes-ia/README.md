# Plataforma de Assistentes com IA — LLMs, RAG e Agentes

**English:** AI Assistants Platform — LLMs, RAG & Agents

Plataforma de portfólio que simula o uso de LLMs para consultar documentos, analisar texto e apoiar operações internas.

> Status: funcional no caminho Supabase — evolução incremental pelo [`ROADMAP.md`](./ROADMAP.md).

## O que este projeto prova

- pipeline RAG nas Edge Functions: embeddings OpenAI (`text-embedding-3-small`), busca por `match_document_chunks` em pgvector e resposta com `gpt-4o-mini`;
- três agentes com prompt próprio (Document Analyst, Ticket Assistant, Workflow Planner), resposta em JSON;
- frontend React com dashboard, chat, upload, agentes, logs, autenticação e configurações;
- registro de prompt, fontes, tokens, latência e custo estimado em `chat_messages` e `agent_executions`;
- backend FastAPI opcional, com rotas de auth, documentos, chat e agentes — a interface não chama essa API.

## O que **não** é

- Produto enterprise em produção
- Substituto de SOC ou sistema de ticketing
- Plataforma multi-tenant SaaS completa
- Integração com Azure OpenAI
- Runtime de ferramentas que executa ações fora do modelo (as ferramentas citadas pelo agente são rótulos no JSON, salvo a busca vetorial)
- Parser dedicado de PDF, DOCX ou XLSX

## Estado atual

| Item | Valor |
|---|---|
| Projeto (PT) | Plataforma de Assistentes com IA |
| Projeto (EN) | AI Assistants Platform |
| ID prefixo | AP |
| Status | Funcional no caminho Supabase (em evolução) |
| Última etapa concluída | AP.04 — README alinhado ao código |
| Próxima etapa | AP.05 — documentar setup local completo |
| Caminho usado pela UI | React → Supabase (Auth, Postgres, Storage, Edge Functions) → OpenAI |
| Backend | FastAPI presente, não ligado ao frontend |

## Limitações reais

- O cliente em `src/integrations/supabase/client.ts` aponta para um projeto Supabase hospedado. `supabase start` e o `.env.example` não redirecionam a interface para uma stack local.
- O `.env.example` lista variáveis do backend FastAPI (`OPENAI_API_KEY`, `DATABASE_URL`, modelos e chunking). O frontend não lê essas variáveis.
- Chat (`rag-query`) e agentes (`run-agent`) usam `OPENAI_API_KEY` no ambiente da Edge Function. A chave salva em Configurações vai só no corpo de `process-document`.
- TXT e MD são lidos como texto. PDF, DOCX e XLSX passam por um fallback que decodifica o arquivo e remove bytes não textuais — não há parser de layout.
- O chunking agrupa parágrafos e sentenças até uma meta de tokens, com sobreposição. Não usa embeddings para cortar o texto.
- No dashboard, documentos indexados, consultas, tokens do dia, custo e latência média vêm do banco. As barras de “Uso de recursos” (Embeddings, pgvector, LLM calls, Storage) são percentuais fixos na página. A taxa de sucesso calculada no hook é a constante `100` e não aparece na tela.
- Ticket Assistant e Workflow Planner consultam chunks indexados. Document Analyst analisa só o texto enviado, sem busca.
- `docker-compose.yml` sobe Postgres (pgvector), a API FastAPI e o Vite. A interface continua no cliente Supabase e ignora `VITE_API_URL`.
- Dados de demonstração em `src/lib/mockData.ts` definem os cartões dos agentes. Métricas, documentos, chat e logs da interface vêm do Supabase. `mockMetrics`, `initialMessages`, `mockAgentResult` e `mockLogs` não são usados pelas páginas.

O passo a passo para subir a stack do zero fica na etapa AP.05.

## Roadmap

Fases em [`ROADMAP.md`](./ROADMAP.md): Base, Documentação, Testes, Qualidade, Produção.

---

## Problema

Empresas acumulam documentos e chamados espalhados. Este repositório mostra um fluxo de consulta e análise sobre esse material, em escala de portfólio.

## Funcionalidades presentes

- Upload para o Storage `documents`, registro na tabela `documents` e processamento pela função `process-document`
- Chunking, embeddings e gravação em pgvector, com deduplicação por hash do texto
- Busca por similaridade de cosseno e chat que responde só com o contexto recuperado, devolvendo fontes
- Agentes `analyst`, `ticket` e `workflow` pela função `run-agent`
- Página de logs com prompts, tokens, latência e status
- Dashboard com contagens reais de documentos, consultas, tokens, custo e latência

## Arquitetura em uso

```
Browser (React / Vite)
  → Supabase Auth + Postgres (pgvector) + Storage
  → Edge Functions: process-document, rag-query, run-agent
  → API OpenAI (embeddings e chat)
  → linhas em chat_messages / agent_executions
```

O FastAPI em `backend/` repete documentos, chat e agentes contra o Postgres do Compose. Nenhuma página importa essa API.

## Pipeline RAG

1. Upload do arquivo e insert em `documents`
2. Download no Storage e extração de texto (TXT/MD nativos; demais tipos por fallback)
3. Normalização e hash; se o hash já estiver indexado, o documento é marcado sem reembeddar
4. Chunks por parágrafos/sentenças (~600 tokens, teto 800, overlap ~90 tokens)
5. Embeddings `text-embedding-3-small` em lotes
6. `match_document_chunks` (limiar 0,7 no chat; 0,65 nos agentes ticket/workflow; até 4 ou 3 chunks)
7. Prompt com as fontes e conclusão via `gpt-4o-mini`
8. Persistência da resposta, fontes, tokens, latência e custo estimado

## Agents

| Agente | O que o código faz |
|---|---|
| **Document Analyst** | Pede ao modelo um JSON com resumo, pontos-chave, riscos e FAQ. Não busca no índice. |
| **Ticket Assistant** | Busca chunks e pede JSON com política citada, prioridade, prazo e resposta sugerida. |
| **Workflow Planner** | Busca chunks e pede JSON com entendimento, plano e próximas ações. |

Os nomes em `tools_used` misturam a busca real (`document_lookup`, quando há chunks) com rótulos devolvidos pelo modelo. Não há executor que chame essas ferramentas.

## Observabilidade

Gravado no banco para chat e execuções de agente:

- prompt (chat) ou raciocínio JSON (agente)
- documentos/chunks recuperados (fontes no chat; contexto injetado no prompt do agente)
- tokens
- latência em milissegundos
- custo estimado (`gpt-4o-mini` e `text-embedding-3-small`)
- modelo

## Stack

- TypeScript, React, Vite
- Supabase (Auth, Postgres, Storage, Edge Functions)
- PostgreSQL com pgvector
- OpenAI (`gpt-4o-mini`, `text-embedding-3-small`)
- FastAPI e Docker Compose no backend opcional, fora do fluxo da interface

## Como executar o frontend

```bash
npm install
npm run dev
```

Isso sobe o Vite. Auth, dados e funções dependem do projeto Supabase já referenciado no cliente, com `OPENAI_API_KEY` nas Edge Functions para chat e agentes. Sem essa chave, o upload ainda pode enviar a chave salva em Configurações; o chat e os agentes não usam essa chave.

Subir Supabase local, ligar o frontend a ele e usar o Compose como stack da interface não está documentado aqui — é a etapa AP.05. O Compose atual não substitui esse projeto hospedado.

## What this project demonstrates

- Engenharia de um fluxo RAG com pgvector e Edge Functions
- Agentes com saída estruturada e, em dois deles, recuperação de trechos
- Métricas e logs persistidos ao lado da resposta
- Separação explícita entre o caminho que a interface usa e o backend FastAPI opcional
