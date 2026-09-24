# Context-Aware AI Assistant

Assistente de IA sensível ao contexto da interface do usuário. O sistema captura o estado atual da tela e fornece sugestões inteligentes, respostas contextualizadas e automações em tempo real.

> Status: em desenvolvimento — execução incremental pelo [`ROADMAP.md`](./ROADMAP.md).

## O que este projeto prova

- copilot sensível ao contexto de UI via postMessage;
- backend FastAPI com contratos Pydantic;
- integração frontend/backend desacoplada;
- base para copilots corporativos.

## O que **não** é

- RPA enterprise em produção
- Extensão de browser comercial
- Produto SaaS completo no dia 1

## Estado atual

| Item | Valor |
|---|---|
| Projeto | Context-Aware AI Assistant |
| ID prefixo | CAA |
| Status | Em desenvolvimento |
| Última etapa concluída | CAA.00 — repositório criado |
| Próxima etapa | CAA.01 — ambiente Python e `pyproject.toml` |
| Superfície | FastAPI + React (planejado) |

## Roadmap

Fases em [`ROADMAP.md`](./ROADMAP.md): Base, Backend, Frontend, Integração, Produção.

## Visão Geral

Este projeto implementa um copilot que entende o contexto visual e funcional da aplicação onde está integrado, oferecendo assistência proativa baseada no que o usuário está fazendo.

## Stack planejada

- **Frontend**: JavaScript / TypeScript, React / Next.js
- **Backend**: Python (FastAPI)
- **IA**: OpenAI / Azure OpenAI, LangChain / LangGraph
- **Comunicação**: APIs REST, Web Messaging API (postMessage)

## Funcionamento

```text
1. A aplicação envia o estado da tela via postMessage
2. O backend recebe o contexto
3. O contexto é estruturado para o LLM
4. O modelo gera resposta ou ação recomendada
5. O frontend exibe sugestões ou executa automação
```

## Arquitetura planejada

```text
context-aware-ai-assistant/
├── frontend/
│   ├── components/
│   ├── hooks/
│   └── context-listener.js
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── services/
│   │   └── prompts/
├── Dockerfile
└── README.md
```

## Diferenciais Técnicos

- Uso de context-aware AI
- Integração via postMessage (baixo acoplamento)
- Assistência em tempo real
- Aplicação de IA diretamente na interface
- Base para copilots corporativos

## Como executar

Ainda não há código de aplicação implementado.
