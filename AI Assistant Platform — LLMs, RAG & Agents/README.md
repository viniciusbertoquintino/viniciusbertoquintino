# AI Assistant Platform --- LLMs, RAG & Agents

Plataforma de IA Generativa que simula como empresas utilizam LLMs para
automatizar processos, analisar documentos e apoiar operações internas.

------------------------------------------------------------------------

## 🎯 Problema

Empresas lidam com grande volume de documentos, chamados e informações
distribuídas, gerando:

-   alto esforço manual\
-   dificuldade de acesso ao conhecimento\
-   baixa eficiência operacional

------------------------------------------------------------------------

## 💡 Solução

Esta plataforma implementa uma solução baseada em **LLMs, RAG e AI
Agents** para:

-   recuperar conhecimento de documentos\
-   automatizar análise de chamados\
-   auxiliar tomada de decisão\
-   reduzir esforço manual em operações

------------------------------------------------------------------------

## 🚀 Principais Funcionalidades

-   Upload e processamento de documentos\
-   Pipeline completo de RAG com embeddings e pgvector\
-   Busca semântica para recuperação de informações\
-   Chat com respostas baseadas em contexto e fontes\
-   Agentes inteligentes para análise de chamados e suporte operacional\
-   Execução estruturada de tarefas com AI Agents\
-   Observabilidade com logs de prompts, tokens e latência\
-   Dashboard com métricas operacionais

------------------------------------------------------------------------

## 🏗️ Arquitetura

User → Frontend (React / Lovable)\
→ Supabase (Auth, PostgreSQL, Storage, pgvector)\
→ Edge Functions (RAG, Agents)\
→ OpenAI / Azure OpenAI\
→ Response + Logs

------------------------------------------------------------------------

## ⚙️ Arquitetura e Execução

A versão principal da plataforma utiliza:

-   Supabase Auth\
-   PostgreSQL + pgvector\
-   Supabase Storage\
-   Supabase Edge Functions

### Backend opcional (FastAPI)

Utilizado para:

-   processamento pesado\
-   execução avançada de agentes\
-   experimentação com pipelines de IA

------------------------------------------------------------------------

## 🧠 Pipeline RAG

1.  Upload de documento\
2.  Extração e limpeza de texto\
3.  Chunking semântico\
4.  Geração de embeddings\
5.  Armazenamento em pgvector\
6.  Busca semântica\
7.  Construção de contexto\
8.  Resposta com LLM

------------------------------------------------------------------------

## 🤖 Agents

### Document Analyst

-   resumo\
-   pontos-chave\
-   riscos

### Ticket Assistant

-   classificação\
-   resposta sugerida

### Workflow Planner

-   ações\
-   etapas

------------------------------------------------------------------------

## 📊 Observabilidade

-   prompt utilizado\
-   documentos recuperados\
-   tokens\
-   latência\
-   custo estimado

------------------------------------------------------------------------

## 🧪 Diferenciais

-   RAG com pgvector\
-   busca semântica\
-   agentes com execução estruturada\
-   observabilidade completa\
-   arquitetura serverless\
-   cenário corporativo real

------------------------------------------------------------------------

## 🛠️ Stack

-   TypeScript\
-   React\
-   Supabase\
-   PostgreSQL (pgvector)\
-   Edge Functions\
-   OpenAI / Azure OpenAI\
-   Docker

------------------------------------------------------------------------

## ⚡ Como Executar

``` bash
cp .env.example .env
```

``` bash
supabase start
```

``` bash
npm install
npm run dev
```

------------------------------------------------------------------------

## 🎯 What this project demonstrates

-   AI Engineering aplicado\
-   uso real de LLMs em negócios\
-   arquitetura de sistemas com IA\
-   automação inteligente\
-   recuperação de conhecimento com RAG

------------------------------------------------------------------------

## ⭐ Destaque

Projeto focado em engenharia de IA aplicada, simulando uso real em
ambientes corporativos.
