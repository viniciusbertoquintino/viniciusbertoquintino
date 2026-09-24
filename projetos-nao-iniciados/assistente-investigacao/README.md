# Assistente de Investigação

Aplicação Streamlit para **organizar evidências** de investigação: catálogo de arquivos e imagens, metadados, filtros, linha do tempo e export.

O objetivo não é substituir um sistema forense ou de cadeia de custódia. O projeto busca demonstrar organização estruturada de evidências com interface simples e export reprodutível.

> Status: 🚧 Em desenvolvimento — execução incremental pelo `ROADMAP.md`.

## O que este projeto prova

- catálogo de evidências com schema único;
- ingestão local de arquivos e imagens;
- filtros, tags e linha do tempo;
- export JSON/CSV;
- testes de módulo para lógica de negócio.

## O que **não** é

- CMS forense ou cadeia de custódia digital
- Integração com sistemas judiciais
- Análise automática de imagens (visão computacional)

## Arquitetura planejada

```text
Arquivos locais
        |
        v
  EvidenceIngestor
        |
        v
  Schema Evidence (metadados + tags)
        |
   +----+----+----+
   |    |    |    |
   v    v    v    v
Lista Filtro Timeline Export
   |    |    |    |
   +----+----+----+
        |
        v
  UI Streamlit
```

## Stack planejada

- Python 3.12+, Streamlit, Pydantic, `uv`, Pytest, Ruff

## Roadmap

Fases em [`ROADMAP.md`](./ROADMAP.md):

- [ ] Base do repositório
- [ ] Schema e ingestão
- [ ] Interface Streamlit
- [ ] Organização e export
- [ ] Produção

## Estado atual

| Item | Valor |
|---|---|
| Projeto | Assistente de Investigação |
| ID prefixo | IV |
| Status | Em desenvolvimento |
| Última etapa concluída | Nenhuma |
| Próxima etapa | IV.00 — criar repositório e `.gitignore` |
| Superfície | Streamlit |

## Como executar

Ainda não há código de aplicação.

## Telas (planejadas)

| Tela | Descrição | Status |
|---|---|---|
| Home | Status do app e resumo | Planejado |
| Catálogo | Lista de evidências | Planejado |
| Detalhe | Metadados e tags de uma evidência | Planejado |
| Timeline | Linha do tempo | Planejado |
| Export | Download JSON/CSV | Planejado |

## Princípios

1. Organizar, não analisar automaticamente.
2. Uma mudança lógica por commit.
3. Não implementar o futuro.
4. Lógica de negócio testável fora da UI.
5. Testar ingestão e export, não só renderização.
6. Não versionar segredos.
7. Documentar limitações reais.
