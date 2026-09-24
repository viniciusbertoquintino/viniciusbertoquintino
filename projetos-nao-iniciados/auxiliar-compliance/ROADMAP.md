# Projeto CP — Auxiliar de Compliance

## Objetivo

Construir uma ferramenta Streamlit que confere documentos contra checklists de normas e gera achados. O diferencial não é "um checklist bonito", mas **checagem automatizada, achados rastreáveis, avaliação mensurável e interface operacional**.

## Stack sugerida

- Python 3.12+, Streamlit, Pydantic, `uv`, Pytest, Ruff

## Microetapas

### Fase 0 — Base do repositório

- [ ] **CP.00** Criar repositório e `.gitignore`.
  - Pronto quando: `main` possui README mínimo e primeiro commit.
- [ ] **CP.01** Criar ambiente Python e `pyproject.toml`.
  - Pronto quando: dependências instalam do zero com `uv sync`.
- [ ] **CP.02** Criar estrutura `app/`, `tests/`, `data/`.
  - Pronto quando: imports funcionam sem hacks de path.
- [ ] **CP.03** Configurar variáveis com `.env.example`.
  - Pronto quando: nenhum segredo está versionado.
- [ ] **CP.04** Criar app Streamlit mínimo com página home e status ok.
  - Pronto quando: `streamlit run app/main.py` inicia sem erro; teste de módulo passa.

### Fase 1 — Schema, loader e checklist

- [ ] **CP.05** Criar schemas `NormCheck`, `Finding`, `Severity` e `ComplianceResult`.
  - Pronto quando: modelos Pydantic validam entrada e saída.
- [ ] **CP.06** Criar `DocumentLoader` para texto (txt, md).
  - Pronto quando: arquivo de texto retorna conteúdo com teste.
- [ ] **CP.07** Criar checklist versionado em `data/checklists/`.
  - Pronto quando: há pelo menos 1 checklist com 10 itens verificáveis.
- [ ] **CP.08** Criar documentos de exemplo em `data/sample/`.
  - Pronto quando: há pelo menos 3 documentos (conforme, parcial, não conforme).

### Fase 2 — Motor de checagem

- [ ] **CP.09** Criar interface `ComplianceChecker`.
  - Pronto quando: núcleo não importa SDK de vendor.
- [ ] **CP.10** Implementar `RuleBasedChecker` (regras por item do checklist).
  - Pronto quando: documento conforme passa; não conforme gera achados com teste.
- [ ] **CP.11** Implementar severidade por achado (info, warning, critical).
  - Pronto quando: achado contém severidade e referência ao item do checklist.

### Fase 3 — Interface e avaliação

- [ ] **CP.12** Criar tela de upload e checagem.
  - Pronto quando: upload de documento executa checagem e exibe resultado.
- [ ] **CP.13** Criar tela de achados com filtros por severidade.
  - Pronto quando: lista de findings filtrável na UI.
- [ ] **CP.14** Criar dataset de avaliação com achados esperados.
  - Pronto quando: há pares documento/achados esperados reprodutíveis.
- [ ] **CP.15** Criar script de avaliação (precisão por item).
  - Pronto quando: métricas são reprodutíveis.

### Fase 4 — LLM opcional e produção

- [ ] **CP.16** Criar interface `LLMProvider` para itens ambíguos.
  - Pronto quando: núcleo não depende de SDK específico.
- [ ] **CP.17** Integrar LLM para checagem de itens textuais complexos.
  - Pronto quando: item ambíguo aciona LLM com resultado rastreável.
- [ ] **CP.18** Criar Dockerfile para app Streamlit.
  - Pronto quando: container sobe e app responde.
- [ ] **CP.19** Criar GitHub Actions para lint + tests.
  - Pronto quando: pipeline roda em PR.
- [ ] **CP.20** Finalizar README com métricas reais.
  - Pronto quando: métricas documentadas foram medidas.

## Resultado que este projeto deve provar

- Você sabe automatizar conferência documento × norma.
- Você gera achados rastreáveis com severidade.
- Você mede precisão por item de checklist.
- Você separa regras de vendor (LLM) na borda.
