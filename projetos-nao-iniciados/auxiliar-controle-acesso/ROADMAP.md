# Projeto AC — Auxiliar de Controle de Acesso

## Objetivo

Construir uma ferramenta Streamlit que analisa registros de acesso em lote e gera relatório de fora de padrão. O diferencial não é "um BI genérico", mas **análise batch de logs, regras configuráveis, relatório exportável e testes reprodutíveis**.

**Distinção:** este projeto (AC) é análise **batch** de registros. O projeto `controle-acesso-inteligente` (CA) é API de **eventos em tempo real**.

## Stack sugerida

- Python 3.12+, Streamlit, Pydantic, `uv`, Pytest, Ruff

## Microetapas

### Fase 0 — Base do repositório

- [ ] **AC.00** Criar repositório e `.gitignore`.
  - Pronto quando: `main` possui README mínimo e primeiro commit.
- [ ] **AC.01** Criar ambiente Python e `pyproject.toml`.
  - Pronto quando: dependências instalam do zero com `uv sync`.
- [ ] **AC.02** Criar estrutura `app/`, `tests/`, `data/`.
  - Pronto quando: imports funcionam sem hacks de path.
- [ ] **AC.03** Configurar variáveis com `.env.example`.
  - Pronto quando: nenhum segredo está versionado.
- [ ] **AC.04** Criar app Streamlit mínimo com página home e status ok.
  - Pronto quando: `streamlit run app/main.py` inicia sem erro; teste de módulo passa.

### Fase 1 — Schema e loader

- [ ] **AC.05** Criar schemas `AccessRecord`, `AnomalyReport`, `AnomalyType`.
  - Pronto quando: modelos Pydantic validam registro e anomalia.
- [ ] **AC.06** Criar `AccessLogLoader` para CSV.
  - Pronto quando: CSV com colunas padrão retorna lista de `AccessRecord` com teste.
- [ ] **AC.07** Criar logs sintéticos de exemplo em `data/sample/`.
  - Pronto quando: há pelo menos 2 CSVs (normal e com anomalias conhecidas).

### Fase 2 — Regras de análise

- [ ] **AC.08** Criar interface `AccessAnalyzer`.
  - Pronto quando: núcleo não importa SDK de vendor.
- [ ] **AC.09** Implementar regra de acesso fora de horário.
  - Pronto quando: registro fora da janela configurada aparece no relatório com teste.
- [ ] **AC.10** Implementar regra de frequência alta por credencial.
  - Pronto quando: credencial com N acessos em janela aparece no relatório com teste.
- [ ] **AC.11** Implementar regra de área rara para credencial.
  - Pronto quando: acesso a área incomum para credencial aparece no relatório com teste.
- [ ] **AC.12** Criar agregador de anomalias por registro.
  - Pronto quando: um lote de registros retorna `AnomalyReport` unificado.

### Fase 3 — Interface e export

- [ ] **AC.13** Criar tela de upload e resumo da análise.
  - Pronto quando: upload de CSV exibe total de registros e anomalias encontradas.
- [ ] **AC.14** Criar tela de relatório com filtros por tipo de anomalia.
  - Pronto quando: lista filtrável na UI.
- [ ] **AC.15** Implementar export do relatório em CSV.
  - Pronto quando: botão gera CSV com anomalias e metadados.
- [ ] **AC.16** Criar script de avaliação com logs rotulados.
  - Pronto quando: precisão por tipo de anomalia é reprodutível.

### Fase 4 — Produção

- [ ] **AC.17** Adicionar testes de borda (CSV vazio, colunas faltando).
  - Pronto quando: casos de borda cobertos.
- [ ] **AC.18** Criar Dockerfile para app Streamlit.
  - Pronto quando: container sobe e app responde.
- [ ] **AC.19** Criar GitHub Actions para lint + tests.
  - Pronto quando: pipeline roda em PR.
- [ ] **AC.20** Finalizar README com métricas reais.
  - Pronto quando: métricas documentadas foram medidas.

## Resultado que este projeto deve provar

- Você sabe analisar logs de acesso em lote com regras configuráveis.
- Você gera relatório de anomalias exportável.
- Você mede precisão com logs sintéticos rotulados.
- Você separa análise batch (AC) de API de eventos (CA).
