# AI Assistant Platform — LLMs, RAG & Agents

Plataforma corporativa de IA Generativa para análise de documentos, automação de processos e suporte operacional utilizando LLMs, RAG (Retrieval-Augmented Generation) e agentes inteligentes.

---

## 🚀 Visão Geral

Este projeto simula um cenário real de aplicação de IA em ambientes corporativos, permitindo que usuários consultem documentos, automatizem tarefas e utilizem assistentes inteligentes integrados a fluxos de trabalho.

A plataforma foi construída com foco em engenharia de IA aplicada, incluindo:

- RAG com busca semântica e híbrida  
- agentes inteligentes com reasoning estruturado  
- memória de conversação  
- observabilidade completa (tokens, latência, custo)  
- arquitetura escalável baseada em Supabase  

---

## 🧠 Principais Funcionalidades

- 📄 Upload e indexação de documentos (PDF, DOCX, XLSX, TXT)
- 🔎 Busca semântica com embeddings (pgvector)
- 💬 Chat com documentos (RAG)
- 📚 Respostas com fontes citadas (grounded answers)
- 🤖 Agentes inteligentes (análise, classificação, workflow)
- 🔄 Automação de processos e workflows
- 📊 Dashboard com métricas em tempo real
- 📜 Logs detalhados (prompt, tokens, latência, custo)
- 🧠 Memória de conversação

---

## 🧩 Casos de Uso

- Consulta a políticas internas  
- Base de conhecimento corporativa  
- Atendimento assistido  
- Análise de documentos  
- Classificação e priorização de chamados  
- Copilot para operações internas  

---

## 🏗️ Arquitetura

Frontend (Lovable UI)
        |
        v
Supabase (Auth, DB, Storage, pgvector)
        |
        v
Edge Functions
        |
        |-- Document Processing (RAG ingestion)
        |-- RAG Query Engine
        |-- Agents Engine
        |
        v
OpenAI / Azure OpenAI

---

## ⚙️ Arquitetura e Execução

A versão principal da plataforma é baseada em Supabase, utilizando:

- Supabase Auth (autenticação)
- PostgreSQL + pgvector (armazenamento e busca vetorial)
- Supabase Storage (upload de documentos)
- Supabase Edge Functions (processamento de documentos, RAG e execução de agentes)

Essa abordagem permite uma arquitetura serverless, simples e escalável para aplicações de IA.

### Backend opcional (FastAPI)

O projeto também inclui uma camada backend em FastAPI, utilizada como extensão para:

- processamento mais pesado de documentos
- execução avançada de agentes
- experimentação com pipelines de IA
- cenários fora das limitações das Edge Functions

Essa camada é opcional e pode ser usada para evolução futura da plataforma.

---

## 🧠 Pipeline RAG

1. Upload de documento  
2. Extração e limpeza de texto  
3. Chunking semântico  
4. Geração de embeddings  
5. Armazenamento em pgvector  
6. Busca semântica e ranking  
7. Construção de contexto  
8. Geração de resposta com LLM  

---

## 🤖 Agents

### Document Analyst

- resumo
- extração de pontos-chave
- identificação de riscos
- geração de FAQ

### Ticket Assistant

- classificação de prioridade
- identificação de área responsável
- sugestão de resposta

### Workflow Planner

- decomposição de tarefas
- sugestão de ações
- simulação de execução

Todos os agentes utilizam:

- RAG para contexto  
- reasoning estruturado  
- resposta em JSON  

---

## 📊 Observabilidade

Cada interação registra:

- prompt utilizado  
- documentos recuperados  
- tokens consumidos  
- latência  
- custo estimado  
- modelo utilizado  

---

## 🧪 Diferenciais Técnicos

- RAG com busca híbrida (semantic + keyword)
- chunking semântico
- memória de conversação
- observabilidade completa
- estimativa de custo por request
- agentes com reasoning estruturado
- fallback anti-alucinação
- arquitetura modular

---

## 🛠️ Stack

### Backend

- Supabase (PostgreSQL + pgvector)
- Supabase Edge Functions (Deno)
- FastAPI (opcional)

### IA

- OpenAI / Azure OpenAI
- Embeddings: text-embedding-3-small
- LLM: gpt-4o-mini

### Frontend

- Lovable / React

### Infra

- Docker (opcional)
- GitHub Actions (CI/CD)

---

## 📁 Estrutura do Projeto

ai-assistant-platform/
├── supabase/
│   ├── functions/
│   ├── migrations/
│   └── config.toml
├── backend/ (opcional)
├── frontend/
├── docs/
├── docker-compose.yml
├── .env.example
└── README.md

---

## ⚡ Como Executar

### 1. Variáveis de ambiente

cp .env.example .env

Adicionar:

OPENAI_API_KEY=your_key
SUPABASE_URL=your_url
SUPABASE_ANON_KEY=your_key

---

### 2. Rodar Supabase

supabase start

---

### 3. Rodar frontend

npm install
npm run dev

---

### 4. (Opcional) Backend

docker-compose up

---

## 🔐 Segurança

- Variáveis sensíveis não expostas ao frontend  
- Uso de Edge Functions para chamadas à API  
- RLS (Row Level Security) configurado  

---

## 🗺️ Roadmap

- Evaluation layer avançada  
- feedback do usuário  
- cache de embeddings  
- tool calling real  
- multi-tenant  

---

## 🎯 Objetivo

Demonstrar aplicação real de IA Generativa em cenários corporativos, com foco em engenharia, automação e impacto de negócio.

---

## ⭐ Destaque

Projeto desenvolvido com foco em AI Engineering aplicado, simulando um ambiente corporativo real com LLMs, RAG e agentes inteligentes.
