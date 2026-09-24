# Projeto CAA — Context-Aware AI Assistant

## Objetivo

Construir um copilot sensível ao contexto da interface do usuário, que recebe estado da tela via postMessage e gera sugestões contextualizadas.

## Stack sugerida

- Python 3.12+, FastAPI, React/Next.js, LangChain, `uv`, Pytest, Ruff

## Microetapas

### Fase 0 — Base do repositório

- [x] **CAA.00** Criar repositório e `.gitignore`.
  - Pronto quando: `main` possui README mínimo e primeiro commit.
- [ ] **CAA.01** Criar ambiente Python e `pyproject.toml`.
  - Pronto quando: dependências instalam do zero com `uv sync`.
- [ ] **CAA.02** Criar estrutura `backend/app/`, `tests/`.
  - Pronto quando: imports funcionam sem hacks de path.
- [ ] **CAA.03** Configurar `.env.example`.
  - Pronto quando: nenhum segredo está versionado.
- [ ] **CAA.04** Criar FastAPI com `GET /health`.
  - Pronto quando: retorna 200 e possui teste automatizado.

### Fase 1 — Backend de contexto

- [ ] **CAA.05** Criar schema `UIContext` (Pydantic).
  - Pronto quando: modelo valida estado da tela recebido.
- [ ] **CAA.06** Criar endpoint `POST /context/analyze`.
  - Pronto quando: recebe contexto e retorna sugestão estruturada.
- [ ] **CAA.07** Integrar LLM para geração de respostas contextualizadas.
  - Pronto quando: resposta usa contexto da tela no prompt.

### Fase 2 — Frontend

- [ ] **CAA.08** Criar projeto frontend (React/Next.js).
  - Pronto quando: app inicia sem erro.
- [ ] **CAA.09** Implementar listener postMessage.
  - Pronto quando: captura estado da tela de app host.
- [ ] **CAA.10** Criar painel de sugestões do copilot.
  - Pronto quando: sugestões exibidas em tempo real.

### Fase 3 — Integração

- [ ] **CAA.11** Conectar frontend ao backend.
  - Pronto quando: fluxo completo postMessage → API → sugestão.
- [ ] **CAA.12** Testes de integração do fluxo.
  - Pronto quando: cenário principal coberto.

### Fase 4 — Produção

- [ ] **CAA.13** Memória de sessão opcional.
  - Pronto quando: contexto acumulado entre interações.
- [ ] **CAA.14** Dockerfile e docker-compose.
  - Pronto quando: stack sobe com um comando.
- [ ] **CAA.15** GitHub Actions para lint + tests.
  - Pronto quando: pipeline roda em PR.
- [ ] **CAA.16** Finalizar README com instruções reais.
  - Pronto quando: documentação alinhada ao estado do código.

## Resultado que este projeto deve provar

- Copilot sensível ao contexto de UI via postMessage.
- Backend FastAPI com contratos Pydantic.
- Integração frontend/backend desacoplada.
- Base para copilots corporativos.
