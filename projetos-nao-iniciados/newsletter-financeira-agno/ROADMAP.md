# Projeto NF — Newsletter Financeira com Agno

## Objetivo

Automatizar a geração e envio de newsletters financeiras usando agentes Agno, com qualidade de engenharia incremental.

## Stack sugerida

- Python 3.12+, Agno, OpenAI, Tavily, `uv`, Pytest, Ruff

## Microetapas

### Fase 0 — Base do repositório

- [x] **NF.00** Criar repositório e `.gitignore`.
  - Pronto quando: `main` possui README mínimo e primeiro commit.
- [x] **NF.01** Scripts Agno funcionais (agente, email, pipeline).
  - Pronto quando: `01.agente.py`, `02.email_tool.py`, `03.news_financeira.py` existem.
- [ ] **NF.02** Criar `pyproject.toml` e migrar para `uv`.
  - Pronto quando: `uv sync` instala dependências do zero.
- [ ] **NF.03** Criar estrutura `app/`, `tests/`.
  - Pronto quando: imports funcionam sem hacks de path.
- [ ] **NF.04** Padronizar `.env.example`.
  - Pronto quando: nenhum segredo está versionado.

### Fase 1 — Pipeline

- [ ] **NF.05** Extrair agente para módulo reutilizável.
  - Pronto quando: agente importável e testável.
- [ ] **NF.06** Extrair email tool para módulo com interface clara.
  - Pronto quando: envio mockável em testes.
- [ ] **NF.07** Unificar pipeline em CLI (`newsletter run`).
  - Pronto quando: um comando executa pesquisa + geração + envio.

### Fase 2 — Qualidade

- [ ] **NF.08** Testes unitários para prompt e formatação financeira.
  - Pronto quando: casos principais cobertos.
- [ ] **NF.09** Configurar Ruff e lint.
  - Pronto quando: `ruff check` passa.

### Fase 3 — Produção

- [ ] **NF.10** Agendamento (cron ou GitHub Actions).
  - Pronto quando: newsletter dispara em horário configurável.
- [ ] **NF.11** GitHub Actions para lint + tests.
  - Pronto quando: pipeline roda em PR.
- [ ] **NF.12** Finalizar README com instruções reais.
  - Pronto quando: documentação alinhada ao estado do código.

## Resultado que este projeto deve provar

- Agente Agno especializado em conteúdo financeiro.
- Pipeline automatizado de newsletter.
- Código modular e testável.
