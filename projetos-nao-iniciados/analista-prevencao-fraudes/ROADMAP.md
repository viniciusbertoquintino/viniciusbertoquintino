# Projeto PF — Analista de Prevenção a Fraudes

## Objetivo

Construir uma ferramenta Streamlit que identifica transações suspeitas em datasets sintéticos. O diferencial não é "um dashboard de BI", mas **detecção modular, score agregado, avaliação mensurável e interface operacional**.

## Stack sugerida

- Python 3.12+, Streamlit, Pydantic, `uv`, Pytest, Ruff

## Microetapas

### Fase 0 — Base do repositório

- [ ] **PF.00** Criar repositório e `.gitignore`.
  - Pronto quando: `main` possui README mínimo e primeiro commit.
- [ ] **PF.01** Criar ambiente Python e `pyproject.toml`.
  - Pronto quando: dependências instalam do zero com `uv sync`.
- [ ] **PF.02** Criar estrutura `app/`, `tests/`, `data/`.
  - Pronto quando: imports funcionam sem hacks de path.
- [ ] **PF.03** Configurar variáveis com `.env.example`.
  - Pronto quando: nenhum segredo está versionado.
- [ ] **PF.04** Criar app Streamlit mínimo com página home e status ok.
  - Pronto quando: `streamlit run app/main.py` inicia sem erro; teste de módulo passa.

### Fase 1 — Schema e dataset

- [ ] **PF.05** Criar schemas `Transaction`, `FraudAlert`, `FraudScore`.
  - Pronto quando: modelos Pydantic validam transação e alerta.
- [ ] **PF.06** Criar dataset sintético rotulado em `data/`.
  - Pronto quando: há pelo menos 100 transações com flag de fraude.
- [ ] **PF.07** Criar `TransactionLoader` para CSV.
  - Pronto quando: CSV retorna lista de `Transaction` com teste.

### Fase 2 — Detectores

- [ ] **PF.08** Criar interface `FraudDetector`.
  - Pronto quando: núcleo não importa SDK de vendor.
- [ ] **PF.09** Implementar detector de valor atípico.
  - Pronto quando: transação acima do limiar gera alerta com teste.
- [ ] **PF.10** Implementar detector de frequência anormal.
  - Pronto quando: N transações em janela curta gera alerta com teste.
- [ ] **PF.11** Implementar detector de padrão incomum (horário/local).
  - Pronto quando: transação fora do padrão histórico gera alerta com teste.
- [ ] **PF.12** Criar `ScoreAggregator` que combina detectores.
  - Pronto quando: transação recebe score 0–100 e lista de alertas.

### Fase 3 — Interface e avaliação

- [ ] **PF.13** Criar tela de upload e visualização de transações.
  - Pronto quando: CSV carregado exibe tabela com score.
- [ ] **PF.14** Destacar transações com score acima do limiar.
  - Pronto quando: alertas visíveis na UI com cor/ícone.
- [ ] **PF.15** Criar tela de detalhe de transação suspeita.
  - Pronto quando: clicar em alerta mostra detectores que dispararam.
- [ ] **PF.16** Criar script de avaliação (precisão/recall).
  - Pronto quando: métricas sobre dataset rotulado são reprodutíveis.

### Fase 4 — Produção

- [ ] **PF.17** Adicionar testes de borda (CSV vazio, valor zero).
  - Pronto quando: casos de borda cobertos.
- [ ] **PF.18** Criar Dockerfile para app Streamlit.
  - Pronto quando: container sobe e app responde.
- [ ] **PF.19** Criar GitHub Actions para lint + tests.
  - Pronto quando: pipeline roda em PR.
- [ ] **PF.20** Finalizar README com métricas reais.
  - Pronto quando: métricas documentadas foram medidas.

## Resultado que este projeto deve provar

- Você sabe modelar detecção de fraude de forma modular.
- Você agrega scores de múltiplos detectores.
- Você mede precisão/recall em dataset rotulado.
- Você expõe análise via interface operacional.
