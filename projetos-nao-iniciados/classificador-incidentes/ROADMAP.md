# Projeto CI — Classificador de Incidentes

## Objetivo

Construir um classificador de ocorrências de segurança que sugere prioridade e equipe responsável a partir do texto da ocorrência. O diferencial não é "chamar um LLM", mas mostrar **classificação estruturada, regras testáveis, avaliação mensurável e API de produção**.

## Stack sugerida

- Python 3.12+
- FastAPI
- Pydantic Settings
- `uv`
- Pytest
- Ruff

## Microetapas

### Fase 0 — Base do repositório

- [ ] **CI.00** Criar repositório e `.gitignore`.
  - Pronto quando: `main` possui README mínimo e primeiro commit.
- [ ] **CI.01** Criar ambiente Python e `pyproject.toml`.
  - Pronto quando: dependências instalam do zero com `uv sync`.
- [ ] **CI.02** Criar estrutura `app/`, `tests/`, `data/`.
  - Pronto quando: imports funcionam sem hacks de path.
- [ ] **CI.03** Configurar variáveis com `.env.example`.
  - Pronto quando: nenhum segredo está versionado.
- [ ] **CI.04** Criar FastAPI com `GET /health`.
  - Pronto quando: retorna 200 e possui teste automatizado.

### Fase 1 — Núcleo de classificação

- [ ] **CI.05** Criar schemas `Incident`, `Priority`, `Team` e `ClassificationResult`.
  - Pronto quando: modelos Pydantic validam entrada e saída com type hints.
- [ ] **CI.06** Criar interface `IncidentClassifier`.
  - Pronto quando: aplicação não importa SDK de vendor no núcleo.
- [ ] **CI.07** Implementar `RuleBasedClassifier` (regras determinísticas).
  - Pronto quando: classificação isolada retorna prioridade e equipe para casos de teste fixos.
- [ ] **CI.08** Criar `POST /classify`.
  - Pronto quando: request/response possuem schemas Pydantic e retorna 200 para entrada válida.
- [ ] **CI.09** Adicionar tratamento de erro para entrada inválida e falhas internas.
  - Pronto quando: texto vazio retorna 422; falha interna retorna erro controlado com teste.
- [ ] **CI.10** Incluir confiança e justificativa na resposta.
  - Pronto quando: resposta contém `confidence` (0–1) e `reasoning` não vazio para casos classificados.

### Fase 2 — Qualidade e avaliação

- [ ] **CI.11** Criar dataset rotulado de exemplo em `data/`.
  - Pronto quando: há pelo menos 20 ocorrências com prioridade e equipe esperadas.
- [ ] **CI.12** Criar script de avaliação com matriz de confusão.
  - Pronto quando: script gera métricas reprodutíveis (acurácia por classe).
- [ ] **CI.13** Adicionar testes de borda.
  - Pronto quando: texto vazio, muito longo e ambíguo estão cobertos por testes.

### Fase 3 — LLM opcional

- [ ] **CI.14** Criar interface `LLMProvider`.
  - Pronto quando: núcleo não depende de SDK específico de LLM.
- [ ] **CI.15** Implementar provider para casos ambíguos.
  - Pronto quando: chamada isolada retorna classificação estruturada.
- [ ] **CI.16** Integrar fallback regras → LLM para baixa confiança.
  - Pronto quando: confiança abaixo do limiar aciona LLM e resultado é rastreável.

### Fase 4 — Produção

- [ ] **CI.17** Adicionar logs estruturados com `request_id`.
  - Pronto quando: uma requisição pode ser rastreada nos logs.
- [ ] **CI.18** Adicionar rate limit básico.
  - Pronto quando: abuso simples é controlado com teste ou documentação verificável.
- [ ] **CI.19** Criar Dockerfile e Docker Compose.
  - Pronto quando: `docker compose up` sobe API funcional.
- [ ] **CI.20** Criar GitHub Actions para lint + tests.
  - Pronto quando: pipeline roda automaticamente em PR.
- [ ] **CI.21** Finalizar README com métricas reais do dataset.
  - Pronto quando: métricas documentadas foram medidas, não inventadas.

## Resultado que este projeto deve provar

- Você sabe estruturar classificação de incidentes com contratos claros.
- Você mede qualidade em vez de ajustar no "feeling".
- Você separa regras de negócio de vendor (LLM).
- Você sabe empacotar, testar e expor via API.
