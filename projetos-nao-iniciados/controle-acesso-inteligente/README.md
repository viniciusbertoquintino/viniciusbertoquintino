# Controle de Acesso Inteligente

API para **analisar eventos de acesso** e detectar padrões anômalos: fora de horário, tentativas recorrentes, uso incomum de credenciais e entradas em áreas não autorizadas.

O objetivo não é substituir um sistema de controle físico ou SIEM. O projeto busca demonstrar detecção modular, alertas estruturados e avaliação com logs sintéticos rotulados.

> Status: 🚧 Em desenvolvimento — execução incremental pelo `ROADMAP.md`.

## O que este projeto prova

- normalização de eventos em schema único;
- detectores independentes e agregação de alertas;
- API REST com contratos Pydantic;
- avaliação com dataset de logs rotulados;
- tratamento de erros e limites de produção.

## O que **não** é

- Dashboard empresarial ou painel de operações
- Integração direta com catracas ou leitores biométricos
- SIEM completo

**Nota:** este projeto (CA) analisa **eventos em tempo real via API**. Para análise de **registros em lote**, veja [`auxiliar-controle-acesso`](../auxiliar-controle-acesso).

## Arquitetura planejada

```text
AccessEvent (entrada)
        |
        v
  AccessDetector (interface)
        |
   +----+----+----+----+
   |    |    |    |    |
   v    v    v    v    v
Fora  Rec. Cred Área
horário tent. inus. não aut.
   |    |    |    |    |
   +----+----+----+----+
        |
        v
  AlertAggregator
        |
        v
   POST /analyze
```

## Stack planejada

- Python 3.12+, FastAPI, Pydantic, `uv`, Pytest, Ruff

## Roadmap

Fases em [`ROADMAP.md`](./ROADMAP.md):

- [ ] Base do repositório
- [ ] Núcleo de detecção
- [ ] Agregação e API
- [ ] Qualidade e avaliação
- [ ] Produção

## Estado atual

| Item | Valor |
|---|---|
| Projeto | Controle de Acesso Inteligente |
| ID prefixo | CA |
| Status | Em desenvolvimento |
| Última etapa concluída | Nenhuma |
| Próxima etapa | CA.00 — criar repositório e `.gitignore` |
| Superfície | FastAPI |

## Como executar

Ainda não há código de aplicação.

## API

| Endpoint | Descrição | Status |
|---|---|---|
| `GET /health` | Healthcheck | Planejado |
| `POST /analyze` | Analisar evento(s) de acesso | Planejado |

## Princípios

1. Medir antes de otimizar.
2. Uma mudança lógica por commit.
3. Não implementar o futuro.
4. Um detector por microetapa.
5. Testar comportamento, não só código.
6. Não versionar segredos.
7. Documentar limitações reais.
