# Context-Aware AI Assistant

Assistente de IA sensível ao contexto da interface do usuário. O sistema captura o estado atual da tela e fornece sugestões inteligentes, respostas contextualizadas e automações em tempo real.

## Visão Geral

Este projeto implementa um copilot que entende o contexto visual e funcional da aplicação onde está integrado, oferecendo assistência proativa baseada no que o usuário está fazendo.

## Stack

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

## Estrutura do Projeto

```
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

## Próximos Passos

- [ ] Execução de ações automatizadas (RPA)
- [ ] Memória de sessão
- [ ] Integração com workflows (n8n)
- [ ] Avaliação de respostas
- [ ] Personalização por usuário

## Status

🚧 Em desenvolvimento
