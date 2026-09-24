# Analista de Prevenção a Fraudes

Aplicação Streamlit para **identificar transações e comportamentos suspeitos** em datasets sintéticos: valor atípico, frequência anormal e padrões incomuns.

O objetivo não é substituir um sistema antifraude bancário. O projeto busca demonstrar detecção modular, score agregado e avaliação com dataset rotulado.

> Status: 🚧 Em desenvolvimento — execução incremental pelo `ROADMAP.md`.

## O que este projeto prova

- detecção modular de fraudes (um detector por tipo);
- score agregado com alertas estruturados;
- UI com tabela de transações e destaque de alertas;
- avaliação com dataset sintético rotulado;
- testes de módulo para cada detector.

## O que **não** é

- Sistema antifraude bancário em produção
- Integração com gateways de pagamento
- Machine learning em larga escala no dia 1

## Arquitetura planejada

```text
Transações (CSV/dataset)
        |
        v
  Schema Transaction
        |
        v
  FraudDetector (interface)
        |
   +----+----+----+
   |    |    |    |
   v    v    v    v
Valor Freq. Padrão ...
atípico anormal incomum
   |    |    |    |
   +----+----+----+
        |
        v
  ScoreAggregator
        |
        v
  UI Streamlit (tabela + alertas)
```

## Stack planejada

- Python 3.12+, Streamlit, Pydantic, `uv`, Pytest, Ruff

## Roadmap

Fases em [`ROADMAP.md`](./ROADMAP.md):

- [ ] Base do repositório
- [ ] Schema e dataset
- [ ] Detectores
- [ ] Interface e avaliação
- [ ] Produção

## Estado atual

| Item | Valor |
|---|---|
| Projeto | Analista de Prevenção a Fraudes |
| ID prefixo | PF |
| Status | Em desenvolvimento |
| Última etapa concluída | Nenhuma |
| Próxima etapa | PF.00 — criar repositório e `.gitignore` |
| Superfície | Streamlit |

## Como executar

Ainda não há código de aplicação.

## Telas (planejadas)

| Tela | Descrição | Status |
|---|---|---|
| Home | Status e upload de dataset | Planejado |
| Transações | Tabela com score e alertas | Planejado |
| Detalhe | Análise de transação suspeita | Planejado |

## Princípios

1. Um detector por microetapa.
2. Uma mudança lógica por commit.
3. Não implementar o futuro.
4. Detectores desacoplados na borda.
5. Testar alertas esperados com dataset rotulado.
6. Não versionar segredos.
7. Documentar limitações reais.
