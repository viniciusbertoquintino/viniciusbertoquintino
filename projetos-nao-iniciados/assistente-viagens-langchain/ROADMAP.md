# Projeto AV — Assistente de Viagens com LangChain

## Objetivo

Evoluir o assistente de viagens via terminal (LangChain + Azure OpenAI) com qualidade de engenharia incremental.

## Stack sugerida

- Python 3.12+, LangChain, Azure OpenAI, `uv`, Pytest, Ruff

## Microetapas

### Fase 0 — Base do repositório

- [x] **AV.00** Criar repositório e `.gitignore`.
  - Pronto quando: `main` possui README mínimo e primeiro commit.
- [x] **AV.01** `app.py` funcional com chat no terminal.
  - Pronto quando: assistente responde perguntas de viagem.
- [x] **AV.02** Criar `pyproject.toml` e migrar para `uv`.
  - Pronto quando: `uv sync` instala dependências do zero.
- [ ] **AV.03** Criar estrutura `app/`, `tests/`.
  - Pronto quando: imports funcionam sem hacks de path.
- [ ] **AV.04** Configurar `.env.example` com variáveis Azure OpenAI.
  - Pronto quando: nenhum segredo está versionado.

### Fase 1 — Refatoração

- [ ] **AV.05** Extrair configuração do modelo para módulo.
  - Pronto quando: config testável e mockável.
- [ ] **AV.06** Extrair loop de chat para módulo reutilizável.
  - Pronto quando: chat testável com mocks.
- [ ] **AV.07** Adicionar histórico de conversa opcional.
  - Pronto quando: contexto mantido entre turnos.

### Fase 2 — Qualidade

- [ ] **AV.08** Testes unitários para parsing de comandos de saída.
  - Pronto quando: 'sair', 'exit', 'tchau' reconhecidos.
- [ ] **AV.09** Configurar Ruff e lint.
  - Pronto quando: `ruff check` passa.

### Fase 3 — Produção

- [ ] **AV.10** Interface web opcional (Streamlit).
  - Pronto quando: app web funcional.
- [ ] **AV.11** GitHub Actions para lint + tests.
  - Pronto quando: pipeline roda em PR.
- [ ] **AV.12** Finalizar README com instruções reais.
  - Pronto quando: documentação alinhada ao estado do código.

## Resultado que este projeto deve provar

- Integração LangChain com Azure OpenAI.
- Chat conversacional especializado em viagens.
- Código modular e testável.
