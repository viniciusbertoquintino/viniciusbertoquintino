# Sistema de Estorno

Projeto que simula o fluxo de estornos (refunds) com regras simples: aprovação para valores altos, processamento com tentativas de retry, fila de DLQ e exportação de dados em JSON.

## 🎯 Principais Funcionalidades

- Branch condicional para aprovação (> R$ 1.000)
- Retry automático (até 2 tentativas, com pequeno atraso)
- Dead Letter Queue (DLQ) e reprocessamento
- Idempotência por `request_id`
- Exportação para JSON
- Menu interativo opcional

## 📦 Requisitos

- Python 3.8+
- Somente bibliotecas padrão

## 🚀 Execução (Windows PowerShell)

- Script principal (demo automática):

```bash
python .\estorno.py
```

## 🗂️ Estrutura

- `estorno.py`: lógica principal e demo

## 🔎 Status possíveis

- `pending`: aguardando processamento/aprovação
- `approved`: aprovado e pronto para processar
- `rejected`: rejeitado pelo aprovador
- `processing`: em processamento
- `completed`: concluído com sucesso
- `failed`: falhou (interno)
- `dlq`: enviado para DLQ após falhas

Tags simples para leitura rápida:

- `[CRIADO]`, `[PROCESSANDO]`, `[SUCESSO]`, `[ERRO]`, `[DLQ]`, `[IDEMPOTENCIA]`

## 📤 Exportação

Ao final da execução/demonstração, os estornos podem ser exportados para um arquivo JSON com timestamp no nome:

**Desenvolvido com bastante dedicação, algumas madrugadas viradas e muito café (risos). Foram exploradas diferentes abordagens de IA para mostrar que não existe uma solução única — tudo depende do contexto específico de cada problema.**