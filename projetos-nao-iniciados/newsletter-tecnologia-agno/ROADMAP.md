# Projeto NT — Newsletter de Tecnologia com Agno

## Objetivo

Automatizar a geração e envio de newsletters de tecnologia usando agentes Agno, com qualidade de engenharia incremental.

## Stack sugerida

- Python 3.12+, Agno, OpenAI, Tavily, `uv`, Pytest, Ruff

## Microetapas

### Fase 0 — Base do repositório

- [x] **NT.00** Criar repositório e `.gitignore`.
  - Pronto quando: `main` possui README mínimo e primeiro commit.
- [x] **NT.01** Scripts Agno funcionais (agente, email, pipeline).
  - Pronto quando: `01.agente.py`, `02.email_tool.py`, `03.news_tech.py` existem.
- [ ] **NT.02** Criar `pyproject.toml` e migrar para `uv`.
  - Pronto quando: `uv sync` instala dependências do zero.
- [ ] **NT.03** Criar estrutura `app/`, `tests/`.
  - Pronto quando: imports funcionam sem hacks de path.
- [ ] **NT.04** Configurar `.env.example`.
  - Pronto quando: nenhum segredo está versionado.

### Fase 1 — Pipeline

- [ ] **NT.05** Extrair agente para módulo reutilizável.
  - Pronto quando: agente importável e testável.
- [ ] **NT.06** Extrair email tool para módulo com interface clara.
  - Pronto quando: envio mockável em testes.
- [ ] **NT.07** Unificar pipeline em CLI (`newsletter run`).
  - Pronto quando: um comando executa pesquisa + geração + envio.

### Fase 2 — Qualidade

- [ ] **NT.08** Testes unitários para prompt e formatação.
  - Pronto quando: casos principais cobertos.
- [ ] **NT.09** Configurar Ruff e lint.
  - Pronto quando: `ruff check` passa.

### Fase 3 — Produção

- [ ] **NT.10** Agendamento (cron ou GitHub Actions).
  - Pronto quando: newsletter dispara em horário configurável.
- [ ] **NT.11** GitHub Actions para lint + tests.
  - Pronto quando: pipeline roda em PR.
- [ ] **NT.12** Finalizar README com instruções reais.
  - Pronto quando: documentação alinhada ao estado do código.

## Resultado que este projeto deve provar

- Agente Agno com ferramentas de pesquisa e email.
- Pipeline automatizado de newsletter de tecnologia.
- Código modular e testável.
