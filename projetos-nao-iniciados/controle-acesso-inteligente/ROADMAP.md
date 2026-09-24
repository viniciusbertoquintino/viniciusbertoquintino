# Projeto CA — Controle de Acesso Inteligente

## Objetivo

Construir uma API que analisa eventos de acesso e detecta anomalias operacionais. O diferencial não é "um dashboard bonito", mas **detecção modular, alertas estruturados, avaliação mensurável e API de produção**.

## Stack sugerida

- Python 3.12+, FastAPI, Pydantic Settings, `uv`, Pytest, Ruff

## Microetapas

### Fase 0 — Base do repositório

- [ ] **CA.00** Criar repositório e `.gitignore`.
  - Pronto quando: `main` possui README mínimo e primeiro commit.
- [ ] **CA.01** Criar ambiente Python e `pyproject.toml`.
  - Pronto quando: dependências instalam do zero com `uv sync`.
- [ ] **CA.02** Criar estrutura `app/`, `tests/`, `data/`.
  - Pronto quando: imports funcionam sem hacks de path.
- [ ] **CA.03** Configurar variáveis com `.env.example`.
  - Pronto quando: nenhum segredo está versionado.
- [ ] **CA.04** Criar FastAPI com `GET /health`.
  - Pronto quando: retorna 200 e possui teste automatizado.

### Fase 1 — Núcleo de detecção

- [ ] **CA.05** Criar schemas `AccessEvent`, `Alert`, `AlertType` e `AnalysisResult`.
  - Pronto quando: modelos Pydantic validam entrada e saída.
- [ ] **CA.06** Criar interface `AccessDetector`.
  - Pronto quando: núcleo não importa SDK de vendor.
- [ ] **CA.07** Implementar detector de acesso fora de horário.
  - Pronto quando: evento fora da janela configurada gera alerta com teste.
- [ ] **CA.08** Implementar detector de tentativas recorrentes.
  - Pronto quando: N tentativas em janela de tempo gera alerta com teste.
- [ ] **CA.09** Implementar detector de credencial incomum.
  - Pronto quando: padrão de uso atípico para credencial gera alerta com teste.
- [ ] **CA.10** Implementar detector de área não autorizada.
  - Pronto quando: acesso a área restrita gera alerta com teste.

### Fase 2 — Agregação e API

- [ ] **CA.11** Criar `AlertAggregator` que combina detectores.
  - Pronto quando: um evento passa por todos os detectores e retorna lista unificada.
- [ ] **CA.12** Criar `POST /analyze` para evento único.
  - Pronto quando: request/response Pydantic e retorna 200 para entrada válida.
- [ ] **CA.13** Suportar análise de lote (`POST /analyze/batch`).
  - Pronto quando: lista de eventos retorna resultados na mesma ordem.
- [ ] **CA.14** Adicionar tratamento de erro para entrada inválida.
  - Pronto quando: evento malformado retorna 422 com teste.

### Fase 3 — Qualidade e avaliação

- [ ] **CA.15** Criar dataset de logs sintéticos rotulados em `data/`.
  - Pronto quando: há pelo menos 30 eventos com alertas esperados.
- [ ] **CA.16** Criar script de avaliação (precisão/recall por tipo de alerta).
  - Pronto quando: métricas são reprodutíveis e documentadas.
- [ ] **CA.17** Adicionar testes de borda.
  - Pronto quando: evento vazio, horário limite e área desconhecida estão cobertos.

### Fase 4 — Produção

- [ ] **CA.18** Adicionar logs estruturados com `request_id`.
  - Pronto quando: requisição rastreável nos logs.
- [ ] **CA.19** Adicionar rate limit básico.
  - Pronto quando: abuso simples é controlado.
- [ ] **CA.20** Criar Dockerfile e Docker Compose.
  - Pronto quando: `docker compose up` sobe API funcional.
- [ ] **CA.21** Criar GitHub Actions para lint + tests.
  - Pronto quando: pipeline roda em PR.
- [ ] **CA.22** Finalizar README com métricas reais.
  - Pronto quando: métricas documentadas foram medidas.

## Resultado que este projeto deve provar

- Você sabe modelar detecção de anomalias de acesso de forma modular.
- Você mede qualidade por tipo de alerta.
- Você expõe análise via API com contratos claros.
- Você sabe empacotar e testar para produção.
