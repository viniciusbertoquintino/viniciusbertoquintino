# Classificador de Incidentes

Sistema para **analisar ocorrências de segurança** e sugerir nível de prioridade (`baixa`, `média`, `alta`, `emergência`) e equipe responsável, a partir do texto da ocorrência.

O objetivo não é substituir um SOC ou sistema de ticketing. O projeto busca demonstrar classificação estruturada, regras testáveis, avaliação com dataset rotulado e caminho claro para API de produção.

> Status: 🚧 Em desenvolvimento — execução incremental pelo `ROADMAP.md`.

## O que este projeto prova

- normalização de ocorrências em schema único;
- classificação desacoplada de vendor (regras primeiro, LLM opcional depois);
- API REST com contratos Pydantic;
- avaliação com métricas reais sobre dataset rotulado;
- testes de borda e tratamento de erros.

## O que **não** é

- SOC completo ou integração com SIEM
- Sistema de tickets ou workflow de escalonamento
- Dashboard empresarial no dia 1

## Arquitetura planejada

A arquitetura será implementada progressivamente ao longo do roadmap.

```text
Texto da ocorrência
        |
        v
  Schema Incident
        |
        v
 IncidentClassifier (interface)
        |
   +----+----+
   |         |
   v         v
Regras    LLMProvider (opcional, fase posterior)
   |         |
   +----+----+
        |
        v
 Priority + Team + confiança + justificativa
        |
        v
   POST /classify
```

## Stack planejada

- Python 3.12+
- FastAPI
- Pydantic / Pydantic Settings
- `uv`
- Pytest
- Ruff

## Roadmap

Desenvolvimento em microetapas verificáveis em [`ROADMAP.md`](./ROADMAP.md).

Fases:

- [ ] Base do repositório
- [ ] Núcleo de classificação
- [ ] Qualidade e avaliação
- [ ] LLM opcional para casos ambíguos
- [ ] Produção

Regra: **uma microetapa concluída = uma validação = um commit lógico** (commit só quando você pedir).

## Estado atual

| Item | Valor |
|---|---|
| Projeto | Classificador de Incidentes |
| ID prefixo | CI |
| Status | Em desenvolvimento |
| Última etapa concluída | Nenhuma |
| Próxima etapa | CI.00 — criar repositório e `.gitignore` |
| Superfície | FastAPI |
| Roadmap | Consulte `ROADMAP.md` |

## Como executar

Ainda não há código de aplicação. Após as microetapas de base, os comandos serão documentados aqui.

## API

| Endpoint | Descrição | Status |
|---|---|---|
| `GET /health` | Healthcheck da API | Planejado |
| `POST /classify` | Classificar ocorrência por texto | Planejado |

## Princípios

1. Medir antes de otimizar — prioridade não se escolhe por feeling.
2. Uma mudança lógica por commit.
3. Não implementar o futuro.
4. Separar classificador de vendor (regras/LLM na borda).
5. Testar comportamento, não só código.
6. Não versionar segredos.
7. Documentar limitações e trade-offs reais.
