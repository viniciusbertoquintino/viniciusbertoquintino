# Sistema de Estorno

Sistema completo de gestão de estornos (refunds) com interface interativa, regras de aprovação automática para valores baixos, processamento com retry automático, e funcionalidades avançadas de monitoramento e exportação.

## 🎯 Principais Funcionalidades

- **Aprovação Automática**: Valores até R$ 1.000 processados automaticamente
- **Aprovação Manual**: Valores acima de R$ 1.000 requerem aprovação de gerente
- **Retry Automático**: Até 2 tentativas de processamento com simulação de falhas
- **Gestão Completa**: Aprovação, rejeição e reprocessamento de estornos
- **Monitoramento**: Listagem filtrada, estatísticas detalhadas e acompanhamento de status
- **Exportação**: Salvamento em JSON com timestamp para auditoria
- **Interface Amigável**: Menu interativo com emojis e feedback visual

## 📦 Requisitos

- Python 3.8+
- Somente bibliotecas padrão

## 🚀 Execução

### Menu Interativo (Recomendado)
```bash
python .\estorno.py
```

O sistema iniciará com um menu interativo completo que permite:
- Criar novos estornos
- Aprovar/rejeitar estornos de valor alto
- Listar estornos com filtros
- Reprocessar estornos com erro
- Visualizar estatísticas
- Salvar dados em arquivo
- Executar demonstração automática

### Demonstração Automática
O menu inclui uma opção de demonstração que cria estornos de exemplo e mostra todo o fluxo do sistema.

## 🗂️ Estrutura

- `estorno.py`: Sistema completo com menu interativo e todas as funcionalidades
- `requirements.txt`: Dependências do projeto (apenas bibliotecas padrão do Python)

## ⚙️ Funcionalidades Detalhadas

### 💰 Gestão de Estornos
- **Criação**: Novos estornos com ID único, valor, cliente e motivo
- **Aprovação Automática**: Valores ≤ R$ 1.000 processados imediatamente
- **Aprovação Manual**: Valores > R$ 1.000 requerem aprovação de gerente
- **Rejeição**: Aprovadores podem rejeitar estornos com justificativa

### 🔄 Processamento e Retry
- **Retry Automático**: Até 2 tentativas de processamento
- **Simulação de Falhas**: Demonstra comportamento em cenários de erro
- **Reprocessamento**: Possibilidade de reprocessar estornos com falha

### 📊 Monitoramento
- **Listagem Filtrada**: Visualizar estornos por status específico
- **Estatísticas Completas**: Contadores por status e valor total
- **Acompanhamento Visual**: Emojis e feedback claro para cada operação

## 🔎 Status dos Estornos

- `pendente`: aguardando processamento/aprovação
- `aprovado`: aprovado e pronto para processar
- `rejeitado`: rejeitado pelo aprovador
- `processando`: em processamento
- `concluido`: concluído com sucesso
- `erro`: falhou após tentativas de retry

### Fluxo de Status
1. **Criação**: Estorno criado com status `pendente`
2. **Aprovação**: Valores > R$ 1.000 precisam aprovação → `aprovado`
3. **Processamento**: Status muda para `processando` durante execução
4. **Resultado**: `concluido` (sucesso) ou `erro` (falha)
5. **Rejeição**: Aprovador pode rejeitar → `rejeitado`

## 📤 Exportação e Persistência

### Salvamento em JSON
- **Formato**: Arquivo JSON com timestamp no nome (`estornos_YYYYMMDD_HHMMSS.json`)
- **Conteúdo**: Todos os estornos com dados completos (ID, valor, cliente, status, datas, etc.)
- **Encoding**: UTF-8 para suporte completo a caracteres especiais
- **Acesso**: Disponível através do menu interativo (opção 7)

### Estrutura do Arquivo JSON
```json
[
  {
    "id": "EST_20250101_143022",
    "valor": 1500.0,
    "cliente": "CLIENTE002",
    "motivo": "Cancelamento de pedido",
    "status": "concluido",
    "data_criacao": "01/01/2025 14:30",
    "aprovador": "GERENTE_SILVA",
    "erro": ""
  }
]
```

---

**Desenvolvido por Vinicius com bastante dedicação. Foram exploradas diferentes abordagens de IA para mostrar que não existe uma solução única — tudo depende do contexto específico de cada problema.**