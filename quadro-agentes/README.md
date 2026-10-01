# Quadro de agentes

Quadro local em que um card de demanda atravessa papéis de agente no Cursor: analista, arquiteto, desenvolvedor, plano de validação e correção depois do teste.

O processo não espera o agente dentro do clique. Ele manda o texto, anota a sessão, pergunta de tempos em tempos se a run acabou e só move o card quando o JSON combinado é válido.

> Status: kit de desenvolvimento. O código da aplicação ainda não existe. A execução segue o [`ROADMAP.md`](./ROADMAP.md), uma microetapa por vez.

## Objetivos técnicos

Ao final do roadmap, a solução deverá demonstrar:

- card com coluna e situação (`queued`, `dispatching`, `analyzing`, `done`, `failed`);
- rodadas com o id do agente, o id da run e o JSON validado;
- um cliente que só cria agente, cria run, lê o agente e lê a run;
- disparo a cada 15 segundos e consulta a cada 30 segundos;
- chat como follow-up na mesma sessão;
- arquiteto, código e plano de testes como o mesmo ciclo, com outro prompt e outra coluna;
- correção que volta ao agente que programou, na mesma branch e no mesmo PR;
- modo mock, para percorrer o quadro sem chave;
- modo live, com `CURSOR_API_KEY`, contra a Cloud Agents API v1.

Nada disso está implementado ainda.

## Arquitetura planejada

A arquitetura entra aos poucos, na ordem do roadmap.

```text
Card (coluna + situação)
        |
        v
Serviço de demanda
  escolhe prompt, modelo e coluna
        |
        +---------------------------+
        |                           |
        v                           v
Timer de disparo (15s)      Chat / follow-up imediato
  claim queued -> dispatching
        |
        v
Cliente HTTP ou mock
  POST /v1/agents
  POST /v1/agents/{id}/runs
        |
        v
Timer de consulta (30s)
  GET agente -> latestRunId
  GET run
        |
        +-- run andando: espera
        +-- erro, cancelamento ou > 1h: failed
        +-- FINISHED + JSON válido: move o card
        +-- texto livre: failed
```

Branch e PR, quando existirem, vêm de `git.branches` da run. Papéis só de leitura usam `mode: "plan"`. Desenvolvedor e correção usam `mode: "agent"` com `autoCreatePR: true`.

Colunas previstas: Backlog, Analisadas pela IA, Validação de desenvolvimento, Implementação e Fila de implantação. Pacote e homologação ficam de fora.

## Stack planejada

- Node.js
- TypeScript
- SQLite (`better-sqlite3`)
- Zod
- Vitest
- página estática servida pelo próprio processo
- Cloud Agents API v1 no modo live

## Roadmap

O desenvolvimento está em microetapas no [`ROADMAP.md`](./ROADMAP.md).

- [ ] Base
- [ ] Telefone e contrato
- [ ] Analista
- [ ] Chat
- [ ] Arquiteto
- [ ] Código e plano de testes
- [ ] Correção
- [ ] Uso

A regra é: **uma microetapa concluída = uma validação**. Commit só quando for pedido. O checkbox de fase acima só fecha quando a fase inteira fecha no roadmap.

## Estado atual

| Item | Valor |
|---|---|
| Projeto | Quadro de agentes |
| Status | Kit de desenvolvimento; aplicação ainda não existe |
| Última etapa concluída | nenhuma |
| Próxima etapa | QA.00 — `package.json`, TypeScript e Vitest |
| Roadmap | `ROADMAP.md` |
| Estratégia | Uma microetapa por vez |
| Commits | Só sob pedido; Conventional Commits; corpo em português e inglês |
| Git | Raiz do perfil, não um repositório dentro desta pasta |
| Stack | Planejada; ainda sem `package.json` |
| Configuração | `.env.example` ainda não existe (QA.01) |
| API Cursor | Ainda não ligada |

> Esta seção acompanha o código. O README não substitui o roadmap.

## Como executar

Ainda não há aplicação para executar. Não existe `package.json`.

Quando a QA.00 estiver concluída, a instalação prevista é:

```bash
cd quadro-agentes
npm install
npm test
```

Esses comandos ainda não fazem parte deste estado. Não os use como se o projeto já rodasse.

Modo mock e modo live, variáveis e a URL local entram no README só quando os passos correspondentes existirem no código.

## API

Nenhum endpoint está implementado.

| Método | Endpoint | Descrição | Status |
|---|---|---|---|
| GET | `/api/board` | Quadro e cards | Planejado (QA.15) |

## Decisões já fixadas

- O cliente HTTP não escolhe coluna, prompt nem modelo.
- Texto livre não move card. Sem o JSON do contrato, a rodada falha.
- Branch e PR vêm de `git.branches`, não do texto do agente.
- O estado da execução está na run (`latestRunId`). O agente pode continuar ativo depois do fim.
- Sem `CURSOR_API_KEY`, o modo mock deve bastar para ver o fluxo. Isso só vale depois da QA.16.
- Segredos não entram no Git.

## Estrutura do projeto

Estado atual, só o kit:

```text
quadro-agentes/
├── .cursor/
│   └── rules/
│       ├── 00-project-context.mdc
│       ├── 10-roadmap-executor.mdc
│       └── 20-git-commit.mdc
├── .gitignore
├── README.md
├── ROADMAP.md
└── SETUP.md
```

Código, testes, prompts, página e `.env.example` aparecem aqui quando as microetapas os criarem.

## Princípios

1. Uma microetapa por vez.
2. O README só descreve o que já existe.
3. JSON combinado ou falha. Sem interpretar texto livre.
4. O telefone não decide o negócio.
5. Não versionar segredos nem o banco local.
6. Commit só quando pedido, e só dos paths da tarefa.

## Autor

**Vinícius Berto**

AI Engineer — IA generativa, LLMs, RAG e agentes.
