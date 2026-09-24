# Auxiliar de Compliance

Aplicação Streamlit para **conferir documentos contra checklists de normas** e gerar lista de achados estruturados.

O objetivo não é substituir uma auditoria certificada. O projeto busca demonstrar checagem automatizada por regras, achados rastreáveis e interface operacional simples.

> Status: 🚧 Em desenvolvimento — execução incremental pelo `ROADMAP.md`.

## O que este projeto prova

- conferência documento × checklist com achados estruturados;
- motor de checagem por regras (LLM opcional depois);
- checklist versionado em `data/`;
- UI de achados com severidade e referência à norma;
- testes de módulo para lógica de checagem.

## O que **não** é

- Sistema de gestão de compliance corporativo
- Auditoria certificada ou laudo formal
- Integração com sistemas de GRC

## Arquitetura planejada

```text
Documento (texto)
        |
        v
  DocumentLoader
        |
        v
  Checklist versionado (data/)
        |
        v
  ComplianceChecker (interface)
        |
   +----+----+
   |         |
   v         v
Regras    LLMProvider (fase posterior)
   |         |
   +----+----+
        |
        v
  Lista de Finding
        |
        v
  UI Streamlit (achados)
```

## Stack planejada

- Python 3.12+, Streamlit, Pydantic, `uv`, Pytest, Ruff

## Roadmap

Fases em [`ROADMAP.md`](./ROADMAP.md):

- [ ] Base do repositório
- [ ] Schema, loader e checklist
- [ ] Motor de checagem
- [ ] Interface e avaliação
- [ ] Produção

## Estado atual

| Item | Valor |
|---|---|
| Projeto | Auxiliar de Compliance |
| ID prefixo | CP |
| Status | Em desenvolvimento |
| Última etapa concluída | Nenhuma |
| Próxima etapa | CP.00 — criar repositório e `.gitignore` |
| Superfície | Streamlit |

## Como executar

Ainda não há código de aplicação.

## Telas (planejadas)

| Tela | Descrição | Status |
|---|---|---|
| Home | Status e upload de documento | Planejado |
| Checagem | Resultado da conferência | Planejado |
| Achados | Lista de findings com severidade | Planejado |

## Princípios

1. Regras primeiro, LLM depois se necessário.
2. Uma mudança lógica por commit.
3. Não implementar o futuro.
4. Checador desacoplado de vendor na borda.
5. Testar achados esperados, não só UI.
6. Não versionar segredos.
7. Documentar limitações reais.
