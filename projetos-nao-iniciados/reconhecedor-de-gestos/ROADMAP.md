# Projeto RG — Reconhecedor de Gestos

## Objetivo

Manter e evoluir uma aplicação de reconhecimento de gestos em tempo real via webcam (MediaPipe + OpenCV), com qualidade de engenharia incremental.

## Stack sugerida

- Python 3.12+, OpenCV, MediaPipe, `uv`, Pytest, Ruff

## Microetapas

### Fase 0 — Base do repositório

- [x] **RG.00** Criar repositório e `.gitignore`.
  - Pronto quando: `main` possui README mínimo e primeiro commit.
- [x] **RG.01** Código base de reconhecimento de gestos funcional.
  - Pronto quando: `gesture_recognizer.py` executa com webcam e detecta gestos.
- [ ] **RG.02** Criar `pyproject.toml` e migrar dependências para `uv`.
  - Pronto quando: `uv sync` instala dependências do zero.
- [ ] **RG.03** Configurar `.env.example` (se necessário) e padronizar `requirements.txt`.
  - Pronto quando: nenhum segredo está versionado.
- [ ] **RG.04** Criar estrutura `app/`, `tests/`.
  - Pronto quando: imports funcionam sem hacks de path.

### Fase 1 — Qualidade

- [ ] **RG.05** Extrair lógica de gestos para módulo testável.
  - Pronto quando: `get_gesture()` possui testes unitários.
- [ ] **RG.06** Adicionar testes para `attention_monitor.py`.
  - Pronto quando: casos principais cobertos com mocks.
- [ ] **RG.07** Configurar Ruff e pipeline local de lint.
  - Pronto quando: `ruff check` passa sem erros.

### Fase 2 — Refatoração

- [ ] **RG.08** Separar captura de vídeo, detecção e renderização.
  - Pronto quando: módulos com responsabilidade única.
- [ ] **RG.09** Adicionar CLI com argumentos (câmera, resolução).
  - Pronto quando: `python -m app` aceita flags documentadas.

### Fase 3 — Produção

- [ ] **RG.10** Criar Dockerfile.
  - Pronto quando: container executa o reconhecedor (com nota sobre webcam).
- [ ] **RG.11** Criar GitHub Actions para lint + tests.
  - Pronto quando: pipeline roda em PR.
- [ ] **RG.12** Finalizar README com métricas e limitações reais.
  - Pronto quando: documentação alinhada ao estado do código.

## Resultado que este projeto deve provar

- Reconhecimento de gestos em tempo real com landmarks.
- Código modular e testável.
- Evolução incremental sem reescrita desnecessária.
