# Agentes e LLM — mesma triagem

## LangGraph (máquina de estados)

Estados e transições condicionais; ramo `humano` para revisão.

```mermaid
stateDiagram-v2
  [*] --> Receber
  Receber --> Classificar
  Classificar --> AvaliarRota
  AvaliarRota --> EncaminharAuto: confianca_alta e nao_emergencia
  AvaliarRota --> RevisaoHumana: confianca_baixa ou emergencia
  RevisaoHumana --> EncaminharAuto: analista_aprovou
  EncaminharAuto --> Auditoria
  Auditoria --> [*]
```

## CrewAI / AutoGen (papéis colaborativos)

Agentes com responsabilidades distintas; setas indicam handoff de artefato (texto estruturado).

```mermaid
flowchart TB
  Entrada[TextoDaOcorrencia]
  AgTriagem[Agente_Triagem]
  AgRelatorio[Agente_Relatorio]
  AgRevisor[Agente_Revisor]
  Saida[PacoteEncaminhamento]

  Entrada --> AgTriagem
  AgTriagem -->|"prioridade equipe confianca"| AgRelatorio
  AgRelatorio -->|"resumo executivo"| AgRevisor
  AgRevisor -->|"aprovado ou corrigido"| Saida
  AgTriagem -->|"confianca baixa"| AgRevisor
```

## Loop conversacional (visão AutoGen)

Dois papéis alternando até critério de parada (stub de multi-turn).

```mermaid
sequenceDiagram
  participant User as Orquestrador
  participant Triagem as AssistenteTriagem
  participant Revisor as AssistenteRevisor

  User->>Triagem: descreva classificacao da ocorrencia
  Triagem-->>User: JSON com prioridade e confianca
  alt confianca menor que limiar
    User->>Revisor: valide ou corrija o JSON
    Revisor-->>User: JSON final
  else confianca ok
    User->>User: usar JSON da triagem
  end
  User->>User: notificar e auditar
```
