# Projeto CS — Chatbot de Orientação em Segurança

## Objetivo

Construir um chatbot de orientação em segurança com respostas fundamentadas em procedimentos versionados. O diferencial não é "um chat genérico", mas **base estruturada, recusa honesta, avaliação de fidelidade e API de produção**.

## Stack sugerida

- Python 3.12+, FastAPI, Pydantic Settings, `uv`, Pytest, Ruff

## Microetapas

### Fase 0 — Base do repositório

- [ ] **CS.00** Criar repositório e `.gitignore`.
  - Pronto quando: `main` possui README mínimo e primeiro commit.
- [ ] **CS.01** Criar ambiente Python e `pyproject.toml`.
  - Pronto quando: dependências instalam do zero com `uv sync`.
- [ ] **CS.02** Criar estrutura `app/`, `tests/`, `data/knowledge/`.
  - Pronto quando: imports funcionam sem hacks de path.
- [ ] **CS.03** Configurar variáveis com `.env.example`.
  - Pronto quando: nenhum segredo está versionado.
- [ ] **CS.04** Criar FastAPI com `GET /health`.
  - Pronto quando: retorna 200 e possui teste automatizado.

### Fase 1 — Base de conhecimento e contrato

- [ ] **CS.05** Criar schemas `ChatRequest`, `ChatResponse`, `KnowledgeEntry`.
  - Pronto quando: modelos Pydantic validam entrada e saída.
- [ ] **CS.06** Criar base de conhecimento em `data/knowledge/` (markdown/FAQ).
  - Pronto quando: há pelo menos 1 documento por tema (6 temas).
- [ ] **CS.07** Criar interface `SecurityChatService`.
  - Pronto quando: núcleo não importa SDK de vendor.
- [ ] **CS.08** Implementar `KeywordMatcher` para respostas diretas.
  - Pronto quando: pergunta com keyword conhecida retorna resposta com fonte.

### Fase 2 — Temas e API

- [ ] **CS.09** Adicionar fixture e teste para tema "senhas".
  - Pronto quando: pergunta sobre senha retorna procedimento correto com fonte.
- [ ] **CS.10** Adicionar fixture e teste para tema "golpes digitais".
  - Pronto quando: pergunta sobre golpe retorna orientação com fonte.
- [ ] **CS.11** Adicionar fixtures para temas restantes (crachá, áreas, incidentes, emergência).
  - Pronto quando: cada tema tem pelo menos 1 teste passando.
- [ ] **CS.12** Implementar recusa para perguntas fora da base.
  - Pronto quando: pergunta sem match retorna recusa explícita com teste.
- [ ] **CS.13** Criar `POST /chat`.
  - Pronto quando: request/response Pydantic e retorna 200 para entrada válida.

### Fase 3 — LLM opcional e qualidade

- [ ] **CS.14** Criar interface `LLMProvider`.
  - Pronto quando: núcleo não depende de SDK específico.
- [ ] **CS.15** Implementar resposta via LLM com contexto da base.
  - Pronto quando: LLM recebe trecho relevante e responde com fonte citada.
- [ ] **CS.16** Criar dataset de avaliação "não inventa política".
  - Pronto quando: há perguntas fora da base com recusa esperada documentada.
- [ ] **CS.17** Criar script de avaliação de fidelidade e recusa.
  - Pronto quando: métricas são reprodutíveis.

### Fase 4 — Produção

- [ ] **CS.18** Adicionar logs estruturados com `request_id`.
  - Pronto quando: requisição rastreável nos logs.
- [ ] **CS.19** Criar Dockerfile e Docker Compose.
  - Pronto quando: `docker compose up` sobe API funcional.
- [ ] **CS.20** Criar GitHub Actions para lint + tests.
  - Pronto quando: pipeline roda em PR.
- [ ] **CS.21** Finalizar README com métricas reais.
  - Pronto quando: métricas documentadas foram medidas.

## Resultado que este projeto deve provar

- Você sabe construir chatbot com base de conhecimento estruturada.
- Você recusa honestamente fora da base.
- Você mede fidelidade e taxa de recusa.
- Você expõe chat via API com contratos claros.
