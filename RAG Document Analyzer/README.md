# RAG Document Analyzer

Sistema de análise de documentos utilizando LLMs e RAG (Retrieval-Augmented Generation) para extração de conhecimento, busca semântica e geração de respostas baseadas em contexto.

## Visão Geral

O RAG Document Analyzer permite o upload e indexação de documentos estruturados e não estruturados (PDF, Word, Excel, TXT), possibilitando consultas inteligentes com base no conteúdo real dos arquivos.

O sistema utiliza embeddings, busca semântica e busca híbrida para recuperar informações relevantes e gerar respostas contextualizadas com LLMs.

## Principais Funcionalidades

- Upload e processamento de documentos
- Extração de texto de múltiplos formatos (PDF, DOCX, XLSX)
- Chunking inteligente de documentos
- Geração de embeddings
- Armazenamento em Vector Database
- Busca semântica (semantic search)
- Busca híbrida (semantic + keyword)
- Geração de respostas com LLMs
- Exibição de fontes utilizadas (grounded answers)

## Casos de Uso

- Consulta a políticas internas
- Análise de documentos corporativos
- Base de conhecimento inteligente
- Suporte operacional
- Atendimento assistido

## Arquitetura

```text
Upload → Parsing → Chunking → Embeddings → Vector DB
                                      ↓
Usuário → Query → Retrieval → Context → LLM → Resposta