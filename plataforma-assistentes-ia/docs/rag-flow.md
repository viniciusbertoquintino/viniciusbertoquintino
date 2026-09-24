# RAG Pipeline — Fluxo detalhado

## Visão geral

```
Upload → Extract → Chunk → Embed → pgvector
Query  → Embed   → Search → Context → LLM → Response + Sources
```

## 1. Indexação (Upload)

| Etapa | Descrição | Parâmetros |
|-------|-----------|-----------|
| `extract_text` | PDF (pdfplumber), DOCX (python-docx), XLSX (openpyxl) | — |
| `chunk_text` | RecursiveCharacter: para em `\n\n`, depois `. `, depois char | size=512, overlap=50 |
| `generate_embedding` | text-embedding-3-small → vetor 1536-dim | batch por chunk |
| `upsert_pgvector` | INSERT INTO document_chunks (embedding vector(1536)) | HNSW index |

## 2. Query (Chat)

| Etapa | Descrição |
|-------|-----------|
| `embed_query` | Mesma função de embedding da indexação |
| `semantic_search` | `1 - (embedding <=> query_vector)` ≥ 0.7, LIMIT 4 |
| `build_context` | Formata os chunks recuperados como contexto |
| `llm_answer` | gpt-4o-mini com system prompt restritivo |

## Prompt de sistema RAG

```
Você é um assistente corporativo especializado em responder perguntas
com base nos documentos da empresa.

Regras:
- Responda APENAS com base nos documentos fornecidos no contexto
- Seja preciso e cite as informações relevantes
- Se a informação não estiver nos documentos, diga claramente
- Use linguagem profissional e direta
```

## pgvector query

```sql
SELECT
    dc.content,
    d.name AS document_name,
    1 - (dc.embedding <=> :query_embedding::vector) AS score
FROM document_chunks dc
JOIN documents d ON dc.document_id = d.id
WHERE 1 - (dc.embedding <=> :query_embedding::vector) >= 0.7
ORDER BY dc.embedding <=> :query_embedding::vector
LIMIT 4;
```

## Índice HNSW

```sql
CREATE INDEX document_chunks_embedding_idx
    ON document_chunks USING hnsw (embedding vector_cosine_ops)
    WITH (m = 16, ef_construction = 64);
```

- `m=16`: conectividade do grafo (trade-off memória vs recall)
- `ef_construction=64`: qualidade do índice na construção
- Recall esperado: ~0.95 com latência <10ms para 1M vetores
