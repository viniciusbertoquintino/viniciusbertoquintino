# Production RAG

Sistema de **Retrieval-Augmented Generation (RAG)** construído como projeto de portfólio de AI Engineering, com foco em práticas próximas de produção.

O objetivo não é apenas criar um chatbot que conversa com documentos. O projeto busca demonstrar, de forma mensurável, qualidade de retrieval, avaliação, observabilidade, custo, latência, testes, segurança básica e deploy.

> Status: 🚧 Em desenvolvimento — execução incremental pelo `ROADMAP.md`.

## Objetivos técnicos

Ao final do projeto, a solução deverá demonstrar:

- ingestão de documentos com rastreabilidade de origem;
- chunking configurável;
- embeddings desacoplados por provider;
- busca vetorial e híbrida;
- reranking opcional;
- respostas fundamentadas com fontes;
- avaliação de retrieval com métricas como Hit@K, Recall@K e/ou MRR;
- avaliação de respostas quanto a relevância e groundedness;
- tracing e observabilidade;
- métricas de latência, tokens e custo;
- testes automatizados e regressão de evals;
- empacotamento com Docker;
- CI/CD;
- deploy em cloud;
- teste de carga e documentação de trade-offs.

## Arquitetura planejada

A arquitetura será implementada progressivamente ao longo do roadmap.

```text
Documents
    |
    v
Ingestion / Loaders
    |
    v
Normalization
    |
    v
Chunking
    |
    v
Embeddings
    |
    v
Vector Database
    |
    +--------------------+
    |                    |
    v                    v
Semantic Search      Lexical Search
    |                    |
    +---------+----------+
              |
              v
        Hybrid Retrieval
              |
              v
          Reranking
              |
              v
         RAG Context
              |
              v
             LLM
              |
              v
       Answer + Sources

Observability / Evals / Metrics
        across the pipeline
```

## Stack planejada

- Python 3.12+
- FastAPI
- Pydantic / Pydantic Settings
- `uv`
- OpenAI ou Azure OpenAI via provider interface
- Qdrant
- Azure AI Search como adaptador opcional
- Pytest
- Ruff
- Langfuse e/ou OpenTelemetry
- Docker / Docker Compose
- GitHub Actions

## Roadmap

O desenvolvimento é dividido em microetapas pequenas e verificáveis no arquivo [`ROADMAP.md`](./ROADMAP.md).

Principais fases:

- [x] Base do repositório
- [x] LLM mínimo
- [x] Ingestão documental
- [ ] Indexação e retrieval
- [ ] Geração fundamentada
- [ ] Qualidade de retrieval
- [ ] Evals de resposta
- [ ] Observabilidade e produção
- [ ] Empacotamento e deploy

A regra do projeto é simples: **uma microetapa concluída = uma validação = um commit lógico**.

## Estado atual

| Item | Valor |
|---|---|
| Projeto | Production RAG |
| Status | Em desenvolvimento |
| Última etapa concluída | P1.18 — script `index_documents.py` |
| Próxima etapa | P1.19 — metadados de origem em cada chunk |
| Roadmap | Consulte `ROADMAP.md` |
| Estratégia | Desenvolvimento incremental |
| Commits | Conventional Commits |
| Python | 3.12+ |
| Gerenciador | `uv` (`pyproject.toml` + `uv.lock`) |
| Ambiente virtual | `.venv/` (criado por `uv sync`) |
| Configuração | `.env.example` → copiar para `.env` (não versionado) |
| LLM | `OpenAIProvider` (`OPENAI_API_KEY`, `OPENAI_MODEL`, `LLM_TIMEOUT_SECONDS`) |
| Documentos de exemplo | `data/sample/` (5 arquivos + PDF + DOCX + CSV + XLSX) |
| Ingestão | loaders retornam `Document` normalizado (`PDFLoader`, `DOCXLoader`, `TabularLoader`); `TextChunker` divide texto com `chunk_size` e `overlap` configuráveis |
| Vector DB | Qdrant local via `docker compose`; collection criada com `scripts/create_qdrant_collection.py` (`QDRANT_URL`, `QDRANT_COLLECTION_NAME`, `QDRANT_VECTOR_SIZE`) |
| Embeddings | `EmbeddingProvider` + `OpenAIEmbeddingProvider` (`OPENAI_EMBEDDING_MODEL`, `EMBEDDING_BATCH_SIZE`) |
| Indexação | `scripts/index_documents.py` carrega PDF/DOCX/CSV/XLSX, faz chunking e grava vetores no Qdrant (`CHUNK_SIZE`, `CHUNK_OVERLAP`) |

> Esta seção deve ser mantida atualizada à medida que o projeto evoluir. O README não substitui o roadmap: ele apresenta o projeto para quem chega ao repositório pela primeira vez.

## Como executar

Requisitos: Python 3.12+, [`uv`](https://docs.astral.sh/uv/) e Docker (para Qdrant local).

```bash
git clone <repository-url>
cd production-rag
uv sync
cp .env.example .env
```

Edite `.env` com seus valores locais. O arquivo `.env` não é versionado; use `.env.example` como referência.

Comandos úteis no estado atual:

```bash
uv run pytest
uv run ruff check .
uv run uvicorn app.main:app --reload
docker compose up -d qdrant
uv run python scripts/create_qdrant_collection.py
uv run python scripts/index_documents.py --input-dir data/sample
```

O Qdrant expõe a API em `http://localhost:6333`. O script de collection é idempotente: cria a collection apenas se ela ainda não existir. A indexação requer `OPENAI_API_KEY` configurada.

Exemplo de chamada ao chat (requer `OPENAI_API_KEY` configurada ou override em testes):

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"Hello"}]}'
```

## API

Os endpoints serão documentados conforme forem implementados.

| Método | Endpoint | Descrição | Status |
|---|---|---|---|
| GET | `/health` | Healthcheck da aplicação | Implementado |
| POST | `/chat` | Chamada ao LLM sem RAG | Implementado (timeout/erros controlados) |
| POST | `/search` | Inspeção do retrieval | Planejado |
| POST | `/ask` | Fluxo completo RAG | Planejado |

## Avaliação

Uma parte central deste projeto é medir o comportamento do sistema em vez de ajustar configurações apenas por percepção subjetiva.

Métricas planejadas:

| Categoria | Métricas |
|---|---|
| Retrieval | Hit@K, Recall@K e/ou MRR |
| Resposta | relevância, groundedness/fidelidade |
| Performance | p50, p95, taxa de erro |
| LLM | tokens, custo aproximado, latência |

Os resultados reais serão adicionados quando as fases de avaliação forem concluídas.

## Resultados e benchmarks

Ainda não disponíveis.

Esta seção será atualizada com medições reais, comparações de configuração e principais trade-offs encontrados durante o projeto.

## Decisões de engenharia

As decisões relevantes serão documentadas conforme surgirem, incluindo temas como:

- escolha de estratégia de chunking;
- busca semântica vs. híbrida;
- uso de reranking;
- critérios de fallback;
- cache;
- custo vs. qualidade;
- latência vs. qualidade;
- acoplamento com provedores;
- observabilidade;
- segurança contra prompt injection.

## Estrutura do projeto

Estrutura atual do repositório:

```text
production-rag/
├── app/
│   ├── api/
│   │   ├── exception_handlers.py
│   │   ├── routes/
│   │   │   └── chat.py
│   │   └── schemas/
│   │       └── chat.py
│   ├── ingestion/
│   │   ├── __init__.py
│   │   ├── chunker.py
│   │   ├── docx_loader.py
│   │   ├── models.py
│   │   ├── pdf_loader.py
│   │   └── tabular_loader.py
│   ├── llm/
│   │   ├── __init__.py
│   │   ├── errors.py
│   │   ├── models.py
│   │   ├── openai_provider.py
│   │   └── provider.py
│   ├── vector/
│   │   ├── __init__.py
│   │   └── qdrant.py
│   ├── embeddings/
│   │   ├── __init__.py
│   │   ├── errors.py
│   │   ├── models.py
│   │   ├── openai_provider.py
│   │   └── provider.py
│   ├── indexing/
│   │   ├── __init__.py
│   │   ├── loaders.py
│   │   ├── models.py
│   │   └── pipeline.py
│   ├── __init__.py
│   ├── dependencies.py
│   ├── main.py
│   └── settings.py
├── tests/
│   ├── __init__.py
│   ├── test_chunker.py
│   ├── test_embedding_provider.py
│   ├── test_indexing_loaders.py
│   ├── test_indexing_pipeline.py
│   ├── test_openai_embedding_provider.py
│   ├── test_qdrant_store.py
│   ├── test_chat.py
│   ├── test_health.py
│   ├── test_imports.py
│   ├── test_llm_provider.py
│   ├── test_openai_provider.py
│   ├── test_openai_provider_errors.py
│   ├── test_docx_loader.py
│   ├── test_document_normalization.py
│   ├── test_pdf_loader.py
│   ├── test_sample_documents.py
│   ├── test_tabular_loader.py
│   ├── test_qdrant_collection.py
│   └── test_settings.py
├── data/
│   └── sample/
│       ├── onboarding-colaboradores.txt
│       ├── politica-ferias.pdf
│       ├── politica-ferias.txt
│       ├── politica-seguranca-informacao.docx
│       ├── politica-seguranca-informacao.md
│       ├── processo-reembolso-despesas.csv
│       ├── processo-reembolso-despesas.txt
│       ├── sla-suporte-interno.md
│       └── sla-suporte-interno.xlsx
├── scripts/
│   ├── create_qdrant_collection.py
│   └── index_documents.py
├── docker-compose.yml
├── .cursor/
│   └── rules/
├── .env.example
├── .gitignore
├── pyproject.toml
├── uv.lock
├── README.md
├── ROADMAP.md
└── SETUP.md
```

O pacote `app` é instalado em modo editável via `uv sync`, permitindo imports sem hacks de `sys.path`. Segredos ficam em `.env`, ignorado pelo Git.

## Princípios do projeto

Este repositório segue alguns princípios desde o início:

1. **Mensurar antes de otimizar.**
2. **Uma mudança lógica por commit.**
3. **Não implementar etapas futuras antes da hora.**
4. **Separar providers de regras de negócio.**
5. **Testar comportamento, não apenas código.**
6. **Não versionar segredos.**
7. **Documentar limitações e trade-offs reais.**

## Autor

**Vinícius Berto**

AI Engineer — Generative AI, LLMs, RAG e AI Agents.
