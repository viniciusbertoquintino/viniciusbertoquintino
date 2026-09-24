# Projeto 1 — Production RAG

## Objetivo
Construir um RAG corporativo demonstrável, executável localmente e com caminho claro para cloud. O diferencial não é “conversar com PDF”, mas mostrar **qualidade de retrieval, avaliação, observabilidade, custo, latência, testes e deploy**.

## Stack sugerida
- Python 3.12+
- FastAPI
- Pydantic Settings
- OpenAI/Azure OpenAI por interface de provider
- Qdrant local como padrão
- Adaptador opcional para Azure AI Search
- Langfuse ou OpenTelemetry para tracing
- Pytest
- Docker / Docker Compose
- GitHub Actions

## Microetapas

### Fase 0 — Base do repositório
- [x] **P1.00** Criar repositório e `.gitignore`.
  - Pronto quando: `main` possui README mínimo e primeiro commit.
- [x] **P1.01** Criar ambiente Python e `pyproject.toml`.
  - Pronto quando: dependências instalam do zero.
- [x] **P1.02** Criar estrutura `app/`, `tests/`, `data/`, `scripts/`.
  - Pronto quando: imports funcionam sem hacks de path.
- [x] **P1.03** Configurar variáveis com `.env.example`.
  - Pronto quando: nenhum segredo está versionado.
- [x] **P1.04** Criar FastAPI com `GET /health`.
  - Pronto quando: retorna 200 e possui teste automatizado.

### Fase 1 — LLM mínimo
- [x] **P1.05** Criar interface `LLMProvider`.
  - Pronto quando: aplicação não depende diretamente de SDK específico.
- [x] **P1.06** Implementar primeiro provider.
  - Pronto quando: uma chamada isolada retorna texto.
- [x] **P1.07** Criar `POST /chat` sem RAG.
  - Pronto quando: request/response possuem schemas Pydantic.
- [x] **P1.08** Adicionar timeout e tratamento de erro do provider.
  - Pronto quando: falha externa vira erro controlado.

### Fase 2 — Ingestão documental
- [x] **P1.09** Criar pasta com documentos públicos/sintéticos de exemplo.
  - Pronto quando: há pelo menos 5 documentos pequenos.
- [x] **P1.10** Criar loader para PDF.
  - Pronto quando: extrai texto + nome do arquivo + página.
- [x] **P1.11** Criar loader para DOCX.
  - Pronto quando: extrai texto + metadados básicos.
- [x] **P1.12** Criar loader para XLSX/CSV.
  - Pronto quando: cada linha/aba gera conteúdo rastreável.
- [x] **P1.13** Normalizar documento em um schema único.
  - Pronto quando: todos os loaders devolvem o mesmo tipo.
- [x] **P1.14** Implementar chunking configurável.
  - Pronto quando: tamanho e overlap são parâmetros.
- [x] **P1.15** Criar teste unitário de chunking.
  - Pronto quando: bordas e documentos vazios estão cobertos.

### Fase 3 — Indexação e retrieval
- [x] **P1.16** Subir Qdrant via Docker Compose.
  - Pronto quando: collection pode ser criada localmente.
- [x] **P1.17** Criar interface `EmbeddingProvider`.
  - Pronto quando: embeddings são desacoplados do fornecedor.
- [x] **P1.18** Criar script `index_documents.py`.
  - Pronto quando: processa documentos e grava vetores.
- [ ] **P1.19** Persistir metadados de origem em cada chunk.
  - Pronto quando: é possível voltar ao arquivo/página original.
- [ ] **P1.20** Implementar busca semântica top-k.
  - Pronto quando: uma query retorna chunks ordenados.
- [ ] **P1.21** Criar endpoint `POST /search`.
  - Pronto quando: retrieval pode ser inspecionado sem geração.
- [ ] **P1.22** Implementar filtros por metadados.
  - Pronto quando: é possível filtrar por tipo/arquivo/categoria.

### Fase 4 — Geração fundamentada
- [ ] **P1.23** Criar prompt RAG mínimo.
  - Pronto quando: modelo recebe pergunta + contexto recuperado.
- [ ] **P1.24** Adicionar regra “não sei” para contexto insuficiente.
  - Pronto quando: resposta não inventa conteúdo fora da base em casos de teste.
- [ ] **P1.25** Incluir citações/fontes na resposta.
  - Pronto quando: API retorna `answer` e lista `sources`.
- [ ] **P1.26** Criar `POST /ask` combinando retrieval + geração.
  - Pronto quando: fluxo completo roda com uma única chamada.

### Fase 5 — Qualidade de retrieval
- [ ] **P1.27** Criar dataset de avaliação em JSONL.
  - Pronto quando: há perguntas, documento esperado e resposta de referência opcional.
- [ ] **P1.28** Medir Hit@K.
  - Pronto quando: script gera métrica reprodutível.
- [ ] **P1.29** Medir Recall@K ou MRR.
  - Pronto quando: relatório compara configurações.
- [ ] **P1.30** Testar pelo menos 3 combinações de chunk size/overlap.
  - Pronto quando: existe tabela com resultados.
- [ ] **P1.31** Implementar busca híbrida.
  - Pronto quando: dense + lexical supera ou é comparado ao baseline.
- [ ] **P1.32** Adicionar reranking opcional.
  - Pronto quando: pode ser ligado/desligado por configuração.

### Fase 6 — Evals de resposta
- [ ] **P1.33** Criar conjunto de respostas esperadas.
  - Pronto quando: existem casos fáceis, ambíguos e sem resposta.
- [ ] **P1.34** Medir groundedness/fidelidade.
  - Pronto quando: avaliação roda automaticamente.
- [ ] **P1.35** Medir relevância da resposta.
  - Pronto quando: relatório possui score por caso.
- [ ] **P1.36** Criar regressão de evals no CI.
  - Pronto quando: queda acima de um limiar falha o pipeline ou gera alerta.

### Fase 7 — Produção
- [ ] **P1.37** Adicionar logs estruturados com `request_id`.
  - Pronto quando: uma requisição pode ser rastreada ponta a ponta.
- [ ] **P1.38** Instrumentar tracing.
  - Pronto quando: retrieval e geração aparecem como spans/steps.
- [ ] **P1.39** Registrar latência por etapa.
  - Pronto quando: retrieval e LLM têm tempos separados.
- [ ] **P1.40** Registrar tokens/custo aproximado.
  - Pronto quando: cada chamada tem consumo observável.
- [ ] **P1.41** Adicionar cache simples.
  - Pronto quando: chamadas repetidas mostram ganho mensurável.
- [ ] **P1.42** Adicionar rate limit básico.
  - Pronto quando: abuso simples é controlado.
- [ ] **P1.43** Adicionar teste de prompt injection básico.
  - Pronto quando: dataset contém ataques e resultado é documentado.

### Fase 8 — Empacotamento e deploy
- [ ] **P1.44** Criar Dockerfile multi-stage ou enxuto.
  - Pronto quando: build é reproduzível.
- [ ] **P1.45** Completar Docker Compose para API + vector DB.
  - Pronto quando: `docker compose up` sobe ambiente funcional.
- [ ] **P1.46** Criar GitHub Actions para lint + tests.
  - Pronto quando: PR roda pipeline automaticamente.
- [ ] **P1.47** Fazer deploy em Azure ou outra cloud.
  - Pronto quando: endpoint remoto responde healthcheck.
- [ ] **P1.48** Executar teste de carga básico.
  - Pronto quando: há p50/p95 e taxa de erro.
- [ ] **P1.49** Criar diagrama de arquitetura.
  - Pronto quando: mostra ingestão, índice, API, LLM, observabilidade.
- [ ] **P1.50** Finalizar README com métricas reais.
  - Pronto quando: um recrutador entende problema, arquitetura, trade-offs e como executar em menos de 3 minutos de leitura.
- [ ] **P1.51** Gravar demo de 60–120 segundos.
  - Pronto quando: mostra busca, fontes e painel de tracing/evals.
- [ ] **P1.52** Publicar post técnico no LinkedIn.
  - Pronto quando: post explica decisão técnica + resultado mensurável, não apenas “fiz um RAG”.

## Resultado que este projeto deve provar
- Você sabe construir RAG end-to-end.
- Você mede retrieval em vez de ajustar no “feeling”.
- Você observa custo/latência.
- Você sabe empacotar, testar e implantar.
