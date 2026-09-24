# Chatbot de Orientação em Segurança

API de chatbot para **orientar colaboradores** sobre procedimentos de segurança: senhas, golpes digitais, perda de crachá, áreas restritas, comunicação de incidentes e procedimentos de emergência.

O objetivo não é substituir treinamento presencial ou políticas corporativas formais. O projeto busca demonstrar respostas fundamentadas em base de conhecimento versionada, recusa honesta fora da base e avaliação de fidelidade.

> Status: 🚧 Em desenvolvimento — execução incremental pelo `ROADMAP.md`.

## O que este projeto prova

- base de conhecimento estruturada e versionada;
- respostas fundamentadas em procedimentos reais;
- recusa explícita para perguntas fora da base;
- avaliação "não inventa política";
- API REST com contratos Pydantic.

## O que **não** é

- RAG com vector database (Qdrant, etc.) no dia 1
- Substituto de treinamento presencial
- Sistema de gestão de políticas corporativas

## Arquitetura planejada

```text
Pergunta do usuário
        |
        v
  KnowledgeBase (FAQ/markdown)
        |
        v
  SecurityChatService (interface)
        |
   +----+----+
   |         |
   v         v
Match      LLMProvider (fase posterior)
direto        |
   |         |
   +----+----+
        |
        v
  Resposta + fonte OU recusa
        |
        v
   POST /chat
```

## Stack planejada

- Python 3.12+, FastAPI, Pydantic, `uv`, Pytest, Ruff

## Roadmap

Fases em [`ROADMAP.md`](./ROADMAP.md):

- [ ] Base do repositório
- [ ] Base de conhecimento e contrato de chat
- [ ] Temas e API
- [ ] Qualidade e avaliação
- [ ] Produção

## Estado atual

| Item | Valor |
|---|---|
| Projeto | Chatbot de Orientação em Segurança |
| ID prefixo | CS |
| Status | Em desenvolvimento |
| Última etapa concluída | Nenhuma |
| Próxima etapa | CS.00 — criar repositório e `.gitignore` |
| Superfície | FastAPI |

## Como executar

Ainda não há código de aplicação.

## API

| Endpoint | Descrição | Status |
|---|---|---|
| `GET /health` | Healthcheck | Planejado |
| `POST /chat` | Pergunta e resposta sobre segurança | Planejado |

## Temas cobertos (planejados)

| Tema | Status |
|---|---|
| Senhas e autenticação | Planejado |
| Golpes digitais | Planejado |
| Perda de crachá | Planejado |
| Áreas restritas | Planejado |
| Comunicação de incidentes | Planejado |
| Procedimentos de emergência | Planejado |

## Princípios

1. Responder só com base no conhecimento versionado.
2. Uma mudança lógica por commit.
3. Não implementar o futuro (RAG só se etapa exigir).
4. Chat desacoplado de vendor na borda.
5. Testar recusa e fidelidade, não só código feliz.
6. Não versionar segredos.
7. Documentar limitações reais.
