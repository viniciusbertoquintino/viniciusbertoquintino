# Projeto RO — Assistente de Relatórios de Ocorrência

## Objetivo

Construir um assistente que transforma anotações operacionais em relatórios estruturados. O diferencial não é "um formulário bonito", mas **extração fiel, campos ausentes honestos, avaliação mensurável e API de produção**.

## Stack sugerida

- Python 3.12+, FastAPI, Pydantic Settings, `uv`, Pytest, Ruff

## Microetapas

### Fase 0 — Base do repositório

- [ ] **RO.00** Criar repositório e `.gitignore`.
  - Pronto quando: `main` possui README mínimo e primeiro commit.
- [ ] **RO.01** Criar ambiente Python e `pyproject.toml`.
  - Pronto quando: dependências instalam do zero com `uv sync`.
- [ ] **RO.02** Criar estrutura `app/`, `tests/`, `data/`.
  - Pronto quando: imports funcionam sem hacks de path.
- [ ] **RO.03** Configurar variáveis com `.env.example`.
  - Pronto quando: nenhum segredo está versionado.
- [ ] **RO.04** Criar FastAPI com `GET /health`.
  - Pronto quando: retorna 200 e possui teste automatizado.

### Fase 1 — Núcleo de extração

- [ ] **RO.05** Criar schema `OccurrenceReport` com todos os campos.
  - Pronto quando: data, horário, local, envolvidos, descrição, medidas e encaminhamentos são campos tipados.
- [ ] **RO.06** Criar interface `ReportExtractor`.
  - Pronto quando: núcleo não importa SDK de vendor.
- [ ] **RO.07** Implementar `RuleBasedExtractor` (parser/regras determinísticas).
  - Pronto quando: extração isolada retorna relatório para anotações de teste fixas.
- [ ] **RO.08** Criar `POST /report`.
  - Pronto quando: request/response Pydantic e retorna 200 para entrada válida.
- [ ] **RO.09** Tratar campos ausentes como `null` ou `"não informado"`.
  - Pronto quando: anotação sem local não inventa local; teste comprova.
- [ ] **RO.10** Adicionar tratamento de erro para entrada inválida.
  - Pronto quando: texto vazio retorna 422 com teste.

### Fase 2 — LLM opcional

- [ ] **RO.11** Criar interface `LLMProvider`.
  - Pronto quando: núcleo não depende de SDK específico.
- [ ] **RO.12** Implementar `LLMReportExtractor` para textos complexos.
  - Pronto quando: chamada isolada retorna `OccurrenceReport` estruturado.
- [ ] **RO.13** Integrar seleção regras → LLM por complexidade.
  - Pronto quando: texto longo ou ambíguo aciona LLM; simples usa regras.

### Fase 3 — Qualidade e avaliação

- [ ] **RO.14** Criar dataset de anotações com relatórios esperados em `data/`.
  - Pronto quando: há pelo menos 15 pares anotação/relatório.
- [ ] **RO.15** Criar script de avaliação de fidelidade por campo.
  - Pronto quando: métricas por campo são reprodutíveis.
- [ ] **RO.16** Adicionar testes de borda.
  - Pronto quando: texto vazio, só data, e texto muito longo estão cobertos.

### Fase 4 — Produção

- [ ] **RO.17** Adicionar logs estruturados com `request_id`.
  - Pronto quando: requisição rastreável nos logs.
- [ ] **RO.18** Criar Dockerfile e Docker Compose.
  - Pronto quando: `docker compose up` sobe API funcional.
- [ ] **RO.19** Criar GitHub Actions para lint + tests.
  - Pronto quando: pipeline roda em PR.
- [ ] **RO.20** Finalizar README com métricas reais de fidelidade.
  - Pronto quando: métricas documentadas foram medidas.

## Resultado que este projeto deve provar

- Você sabe extrair estrutura de texto operacional sem inventar dados.
- Você mede fidelidade por campo.
- Você separa regras de vendor (LLM) na borda.
- Você expõe extração via API com contratos claros.
