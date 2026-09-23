# Orquestração e pipelines — mesma triagem

## Temporal (workflow durável — sequência com retentativas)

Atividades com retry; o workflow mantém estado até concluir.

```mermaid
sequenceDiagram
  participant Client as ClienteAPI
  participant WF as TriagemWorkflow
  participant ActC as Activity_Classificar
  participant ActN as Activity_Notificar
  participant ActA as Activity_Auditar

  Client->>WF: start(textoOcorrencia)
  WF->>ActC: execute com retry
  ActC-->>WF: prioridade equipe confianca
  alt confianca baixa ou emergencia
    WF->>WF: waitSignal(aprovacaoAnalista)
  end
  WF->>ActN: execute com retry
  ActN-->>WF: ok
  WF->>ActA: execute
  ActA-->>WF: idAuditoria
  WF-->>Client: resultadoFinal
```

## Airflow / Prefect (DAG de dados)

Tarefas batch ou micro-batch; dependências explícitas entre tasks.

```mermaid
flowchart LR
  T_extrair[extrair_ocorrencias_pendentes]
  T_normalizar[normalizar_schema]
  T_classificar[classificar_prioridade]
  T_decidir[decidir_auto_ou_fila]
  T_notificar[notificar_equipes]
  T_auditar[persistir_auditoria]

  T_extrair --> T_normalizar
  T_normalizar --> T_classificar
  T_classificar --> T_decidir
  T_decidir --> T_notificar
  T_notificar --> T_auditar
```

## GitHub Actions (analogia de pipeline de entrega)

Jobs em paralelo ou sequência — aqui mapeados como **validar entrada → testar classificador → publicar notificação** (metáfora de CI aplicada ao fluxo).

```mermaid
flowchart TB
  subgraph jobLint [job_validar_entrada]
    L1[checkout]
    L2[validar_json_schema]
    L1 --> L2
  end
  subgraph jobTest [job_classificar]
    T1[pytest_classificador]
    T2[gerar_artifact_resultado]
    T1 --> T2
  end
  subgraph jobDeploy [job_notificar]
    D1[enviar_notificacao]
    D2[registrar_auditoria]
    D1 --> D2
  end
  jobLint --> jobTest
  jobTest --> jobDeploy
```
