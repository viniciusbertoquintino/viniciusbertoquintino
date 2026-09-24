# Projeto IV — Assistente de Investigação

## Objetivo

Construir uma ferramenta Streamlit para organizar evidências de investigação. O diferencial não é "um drive de arquivos", mas **catálogo estruturado, metadados, timeline, filtros e export reprodutível**.

## Stack sugerida

- Python 3.12+, Streamlit, Pydantic, `uv`, Pytest, Ruff

## Microetapas

### Fase 0 — Base do repositório

- [ ] **IV.00** Criar repositório e `.gitignore`.
  - Pronto quando: `main` possui README mínimo e primeiro commit.
- [ ] **IV.01** Criar ambiente Python e `pyproject.toml`.
  - Pronto quando: dependências instalam do zero com `uv sync`.
- [ ] **IV.02** Criar estrutura `app/`, `tests/`, `data/`.
  - Pronto quando: imports funcionam sem hacks de path.
- [ ] **IV.03** Configurar variáveis com `.env.example`.
  - Pronto quando: nenhum segredo está versionado.
- [ ] **IV.04** Criar app Streamlit mínimo com página home e status ok.
  - Pronto quando: `streamlit run app/main.py` inicia sem erro e home exibe status; teste de módulo passa.

### Fase 1 — Schema e ingestão

- [ ] **IV.05** Criar schema `Evidence` com metadados (nome, tipo, data, tags).
  - Pronto quando: modelo Pydantic valida evidência com type hints.
- [ ] **IV.06** Criar `EvidenceIngestor` para arquivos locais.
  - Pronto quando: pasta de entrada retorna lista de `Evidence` com teste.
- [ ] **IV.07** Suportar ingestão de imagens com metadados básicos.
  - Pronto quando: imagem gera `Evidence` com dimensões e formato.
- [ ] **IV.08** Criar pasta `data/sample/` com evidências de exemplo.
  - Pronto quando: há pelo menos 5 arquivos de exemplo ingeríveis.

### Fase 2 — Interface Streamlit

- [ ] **IV.09** Criar tela de catálogo (lista de evidências).
  - Pronto quando: app exibe tabela com nome, tipo e data.
- [ ] **IV.10** Criar tela de detalhe de evidência.
  - Pronto quando: clicar em item mostra metadados e tags editáveis.
- [ ] **IV.11** Implementar filtros por tipo e tag.
  - Pronto quando: filtro reduz lista visível com teste de lógica.

### Fase 3 — Organização e export

- [ ] **IV.12** Implementar linha do tempo por data.
  - Pronto quando: evidências ordenadas por data aparecem em timeline.
- [ ] **IV.13** Implementar busca por texto em nome e tags.
  - Pronto quando: busca retorna subset correto com teste.
- [ ] **IV.14** Implementar export JSON.
  - Pronto quando: botão gera arquivo JSON válido com todas as evidências.
- [ ] **IV.15** Implementar export CSV.
  - Pronto quando: botão gera CSV com colunas de metadados.

### Fase 4 — Produção

- [ ] **IV.16** Adicionar testes de borda (pasta vazia, arquivo corrompido).
  - Pronto quando: casos de borda cobertos por testes.
- [ ] **IV.17** Criar Dockerfile para app Streamlit.
  - Pronto quando: container sobe e app responde.
- [ ] **IV.18** Criar GitHub Actions para lint + tests.
  - Pronto quando: pipeline roda em PR.
- [ ] **IV.19** Finalizar README com comandos reais de execução.
  - Pronto quando: `streamlit run` documentado e testado.

## Resultado que este projeto deve provar

- Você sabe organizar evidências com schema estruturado.
- Você separa lógica de negócio da UI Streamlit.
- Você implementa filtros, timeline e export testáveis.
- Você empacota ferramenta interativa para uso operacional.
