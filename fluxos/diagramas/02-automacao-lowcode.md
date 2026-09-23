# Automação low-code — mesma triagem, três notações

## Estilo n8n (grafo com nós e IF)

Cada caixa equivale a um nó no editor visual; ramificações com nó de condição.

```mermaid
flowchart LR
  Webhook[Webhook_POST] --> Normalize[Set_NormalizarCampos]
  Normalize --> HTTPClassify[HTTP_ClassificarAPI]
  HTTPClassify --> IFConf{IF_Confianca}
  IFConf -->|">= 0.75"| IFEmerg{IF_Emergencia}
  IFConf -->|"< 0.75"| SlackRev[Slack_FilaRevisao]
  IFEmerg -->|nao| Gmail[Gmail_NotificarEquipe]
  IFEmerg -->|sim| SlackRev
  SlackRev --> WaitHuman[Manual_AprovarNoSlack]
  WaitHuman --> Gmail
  Gmail --> Sheets[GoogleSheets_Auditoria]
```

## Estilo Zapier (cadeia linear)

Zaps costumam ler como trigger → ações em sequência; ramificações viram Zaps separados ou Paths (aqui, dois caminhos após um “Path” conceitual).

```mermaid
flowchart TD
  T1["Trigger: Webhooks by Zapier — Catch Hook"]
  T1 --> A1["Action: Formatter — Texto limpo"]
  A1 --> A2["Action: Webhooks — POST classificador"]
  A2 --> P1{"Paths: Confianca OK?"}
  P1 -->|Path A| A3["Action: Slack — Mensagem equipe"]
  P1 -->|Path B| A4["Action: Gmail — Tarefa para analista"]
  A4 --> A5["Action: Slack — Mensagem equipe apos revisao"]
  A3 --> A6["Action: Google Sheets — Nova linha auditoria"]
  A5 --> A6
```

## Estilo Power Automate (gatilho + ações em nuvem)

Subgrafos representam escopo de fluxo cloud e ramo condicional.

```mermaid
flowchart TB
  subgraph fluxoPrincipal [Fluxo_TriagemIncidente]
    Trigger[When_HTTP_request_received]
    Trigger --> Parse[Parse_JSON]
    Parse --> Classify[HTTP_Classificacao]
    Classify --> Condition[Condition_Confianca_e_Prioridade]
    Condition -->|True| SendMail[Send_email_V2]
    Condition -->|False| Approval[Start_and_wait_for_approval]
    Approval --> SendMail
    SendMail --> LogRow[Add_row_Excel_ou_Dataverse]
  end
```
