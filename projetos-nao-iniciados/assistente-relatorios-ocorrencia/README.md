# Assistente de Relatórios de Ocorrência

Sistema para **transformar anotações operacionais** em relatórios estruturados com data, horário, local, envolvidos, descrição, medidas adotadas e encaminhamentos.

O objetivo não é substituir um sistema de gestão de ocorrências. O projeto busca demonstrar extração estruturada, fidelidade ao texto original e API de produção.

> Status: 🚧 Em desenvolvimento — execução incremental pelo `ROADMAP.md`.

## O que este projeto prova

- extração de campos estruturados a partir de texto livre;
- contrato `ReportExtractor` desacoplado de vendor;
- campos ausentes tratados honestamente (sem inventar);
- avaliação de fidelidade com dataset de exemplo;
- API REST com contratos Pydantic.

## O que **não** é

- Sistema de gestão de ocorrências (ticketing)
- Workflow de aprovação ou assinatura digital
- Integração com ERP ou sistemas legados

## Arquitetura planejada

```text
Anotações operacionais (texto)
        |
        v
  ReportExtractor (interface)
        |
   +----+----+
   |         |
   v         v
Regras    LLMProvider (fase posterior)
   |         |
   +----+----+
        |
        v
  OccurrenceReport (schema)
        |
        v
   POST /report
```

## Stack planejada

- Python 3.12+, FastAPI, Pydantic, `uv`, Pytest, Ruff

## Roadmap

Fases em [`ROADMAP.md`](./ROADMAP.md):

- [ ] Base do repositório
- [ ] Núcleo de extração
- [ ] API e tratamento de campos ausentes
- [ ] Qualidade e avaliação
- [ ] Produção

## Estado atual

| Item | Valor |
|---|---|
| Projeto | Assistente de Relatórios de Ocorrência |
| ID prefixo | RO |
| Status | Em desenvolvimento |
| Última etapa concluída | Nenhuma |
| Próxima etapa | RO.00 — criar repositório e `.gitignore` |
| Superfície | FastAPI |

## Como executar

Ainda não há código de aplicação.

## API

| Endpoint | Descrição | Status |
|---|---|---|
| `GET /health` | Healthcheck | Planejado |
| `POST /report` | Extrair relatório estruturado de anotações | Planejado |

## Princípios

1. Fidelidade ao texto original — não inventar campos.
2. Uma mudança lógica por commit.
3. Não implementar o futuro.
4. Extrator desacoplado de vendor na borda.
5. Testar comportamento, não só código.
6. Não versionar segredos.
7. Documentar limitações reais.
