# Auxiliar de Controle de Acesso

Aplicação Streamlit para **analisar registros de acesso em lote** (CSV/log) e gerar relatório de acessos fora de padrão: horário, frequência e áreas incomuns.

O objetivo não é substituir um sistema de controle físico. O projeto busca demonstrar análise batch de logs, regras configuráveis e relatório operacional exportável.

> Status: 🚧 Em desenvolvimento — execução incremental pelo `ROADMAP.md`.

## O que este projeto prova

- ingestão de registros de acesso (CSV/log);
- análise batch com regras de horário e padrão;
- relatório de fora de padrão com filtros;
- export do relatório;
- testes de módulo para lógica de análise.

## O que **não** é

- API de eventos em tempo real (veja [`controle-acesso-inteligente`](../controle-acesso-inteligente))
- Integração com catracas ou leitores biométricos
- SIEM ou dashboard empresarial

**Distinção:** este projeto (AC) analisa **registros em lote via upload**. O projeto CA analisa **eventos em tempo real via API**.

## Arquitetura planejada

```text
Arquivo CSV/log (upload)
        |
        v
  AccessLogLoader
        |
        v
  Schema AccessRecord
        |
        v
  AccessAnalyzer (regras)
        |
   +----+----+----+
   |    |    |    |
   v    v    v    v
Fora  Freq. Área Padrão
horário alta  rara  incomum
   |    |    |    |
   +----+----+----+
        |
        v
  Relatório de anomalias
        |
        v
  UI Streamlit + export
```

## Stack planejada

- Python 3.12+, Streamlit, Pydantic, `uv`, Pytest, Ruff

## Roadmap

Fases em [`ROADMAP.md`](./ROADMAP.md):

- [ ] Base do repositório
- [ ] Schema e loader
- [ ] Regras de análise
- [ ] Interface e export
- [ ] Produção

## Estado atual

| Item | Valor |
|---|---|
| Projeto | Auxiliar de Controle de Acesso |
| ID prefixo | AC |
| Status | Em desenvolvimento |
| Última etapa concluída | Nenhuma |
| Próxima etapa | AC.00 — criar repositório e `.gitignore` |
| Superfície | Streamlit |

## Como executar

Ainda não há código de aplicação.

## Telas (planejadas)

| Tela | Descrição | Status |
|---|---|---|
| Home | Status e upload de log | Planejado |
| Análise | Resumo de registros processados | Planejado |
| Relatório | Acessos fora de padrão com filtros | Planejado |
| Export | Download do relatório | Planejado |

## Princípios

1. Batch, não tempo real — upload e análise.
2. Uma mudança lógica por commit.
3. Não implementar o futuro.
4. Análise testável fora da UI.
5. Testar regras com logs sintéticos rotulados.
6. Não versionar segredos.
7. Documentar limitações reais.
