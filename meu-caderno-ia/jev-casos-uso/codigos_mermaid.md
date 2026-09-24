# Fluxos JEV — códigos Mermaid

## Fluxo 1 — Coding Agent + JEV Eval

```mermaid
flowchart TD
    A[Coding Agent] --> B[Diff + testes + logs]
    B --> C{JEV Eval}

    C -->|PASS| D[Pass]
    C -->|RETRY| E[Retry]
    C -->|HUMAN| F[Human]

    E --> G[Feedback operacional<br/>Falha + evidência + ação recomendada]
    G --> A
```

## Fluxo 2 — Loop agêntico para agendar uma consulta

```mermaid
flowchart LR
    A["REQUEST<br/>Agende um dermatologista<br/>na semana que vem à tarde"]
        --> B["1. ESTADO DO AGENTE<br/>Objetivo + contexto<br/>Histórico + restrições"]

    B --> C{"JEV<br/>Qual é a próxima ação?"}
    C -->|SEARCH_SLOT| D["2. TOOL CALL<br/>Buscar disponibilidade"]
    D --> E["3. OBSERVAÇÃO<br/>Horários encontrados"]
    E --> F["4. NOVO ESTADO<br/>Memória atualizada"]
    F --> G{"JEV<br/>Próximo passo?"}
    G -->|NEED_USER| H["5. ASK USER<br/>Encontrei 3 horários.<br/>Qual você prefere?"]
    H --> I["USUÁRIO<br/>Quarta às 16:30"]
    I --> J["6. ESTADO ATUALIZADO<br/>Horário escolhido"]
    J --> K{"JEV<br/>Próxima ação?"}
    K -->|BOOK_SLOT| L["7. TOOL CALL<br/>Reservar horário"]
    L --> M["8. OBSERVAÇÃO<br/>Reserva confirmada"]
    M --> N{"JEV<br/>Terminou?"}
    N -->|DONE| O["9. RESPOSTA FINAL<br/>Consulta confirmada<br/>quarta às 16:30"]

    E -. "resultado vira novo estado" .-> C
```

## Fluxo 3 — Orquestração de agentes

```mermaid
flowchart TD
    A["Issue<br/>Checkout 500"] -->|Estado atual| B{"JEV Router<br/>Quem trabalha agora?"}

    B --> C[Researcher]
    B --> D[Coder]
    B --> E[Tester]
    B --> F[Reviewer]

    C -->|Novo estado| B
    D -->|Novo estado| B
    E -->|Novo estado| B
    F -->|Novo estado| B
```

## Fluxo 4 — Orquestração de modelos

```mermaid
flowchart TD
    A["Budget<br/>US$ 1,00"] --> B[Subtask]
    B --> C{"JEV<br/>Model Router"}

    C -->|Barato| D[Small]
    C -->|Especialista| E[Coding]
    C -->|Difícil| F[Frontier]

    D --> G[Execução]
    E --> G
    F --> G

    H["Princípio:<br/>não escolher sempre o melhor modelo<br/>alocar inteligência faz parte da arquitetura"]
```

## Fluxo 5 — Triagem

```mermaid
flowchart TD
    A[Email] --> E{"JEV<br/>Triagem"}
    B[Bug] --> E
    C[Lead] --> E
    D[Alerta] --> E

    E --> F[Critical Bug]
    E --> G[Sales Lead]
    E --> H[Feature Request]

    F --> I[Incident Workflow]
    G --> J[CRM + Follow-up]
    H --> K[Backlog]
```

## Fluxo 6 — Benchmark

```mermaid
flowchart TD
    A["Mesmas tarefas<br/>Bugs + Features + Research + Refactor"] --> B{Test Harness}

    B --> C[Arquitetura A]
    B --> D[Arquitetura B + JEV]

    C --> E[Medição]
    D --> E

    E --> F[Success Rate]
    E --> G[Cost]
    E --> H[Latency]
    E --> I[Retries]
    E --> J[Human Intervention]
```
