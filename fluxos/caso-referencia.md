# Caso de referência — triagem de incidente

Cenário fictício usado em todos os diagramas da pasta `fluxos/`.

## Objetivo

Receber a descrição de uma ocorrência de segurança, sugerir **prioridade** e **equipe responsável**, decidir se o encaminhamento é automático ou passa por **revisão humana**, e registrar trilha de **auditoria**.

## Atores

| Ator | Papel |
|------|--------|
| Operador | Registra ou encaminha o texto da ocorrência (formulário, e-mail, integração). |
| Sistema | Normaliza entrada, classifica, notifica e persiste auditoria. |
| Analista | Revisa casos de baixa confiança ou prioridade crítica antes do encaminhamento final. |

## Fluxo lógico

1. **Entrada** — texto da ocorrência via webhook, formulário ou API.
2. **Classificação** — prioridade: `baixa`, `média`, `alta`, `emergência`; equipe sugerida (ex.: facilities, TI, segurança patrimonial).
3. **Decisão** — se confiança da classificação é alta **e** prioridade não exige escalonamento imediato → encaminhar; caso contrário → fila de revisão humana.
4. **Saída** — notificação (e-mail ou Slack) à equipe + registro imutável de auditoria (quem/o quê/quando).

## Entradas e saídas (contrato conceitual)

**Entrada (exemplo):**

```json
{
  "texto": "Porta do almoxarifado encontrada aberta após o horário.",
  "origem": "formulario_web",
  "local": "Bloco B"
}
```

**Saída (exemplo):**

```json
{
  "prioridade": "alta",
  "equipe": "seguranca_patrimonial",
  "confianca": 0.82,
  "requer_revisao": false,
  "id_auditoria": "aud-2026-0001"
}
```

## Glossário

| Termo | Significado |
|-------|-------------|
| Confiança | Score (0–1) de que a classificação automática está correta. |
| Revisão humana | Analista confirma ou corrige prioridade/equipe antes de notificar. |
| Auditoria | Registro append-only para conformidade e pós-incidente. |

## Diagramas derivados

Cada arquivo em [diagramas/](diagramas/) mostra o **mesmo** roteiro com a mentalidade de um tipo de ferramenta (low-code, orquestração, agentes LLM, etc.).
