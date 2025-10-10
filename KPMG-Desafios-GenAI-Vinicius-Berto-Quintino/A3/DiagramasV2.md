# 📊 Diagramas - Sistema Completo de Gestão de Estornos

Este documento contém os diagramas que representam o fluxo completo do sistema de estornos implementado, incluindo todas as funcionalidades do menu interativo.

## 🔄 Fluxo Principal de Processamento

```mermaid
flowchart TD
    A[Criar Estorno] --> B{Valor > R$ 1.000?}
    B -->|Não| C[Processar Automaticamente]
    B -->|Sim| D[Status: pendente]
    D --> E[Aguardar Aprovação Manual]
    E --> F{Aprovado?}
    F -->|Sim| G[Status: aprovado]
    F -->|Não| H[Status: rejeitado]
    G --> I[Status: processando]
    C --> I
    I --> J[Simular Processamento]
    J --> K{Sucesso na 1ª tentativa?}
    K -->|Sim| L[Status: concluido]
    K -->|Não| M[2ª Tentativa]
    M --> N{Sucesso na 2ª tentativa?}
    N -->|Sim| L
    N -->|Não| O[Status: erro]
    O --> P[Reprocessamento Manual]
    P --> I
    H --> Q[Fim - Rejeitado]
    L --> R[Fim - Concluído]
```

## 📋 Estados do Estorno

```mermaid
stateDiagram-v2
    [*] --> pendente
    pendente --> processando : Valor ≤ R$ 1.000
    pendente --> aprovado : Valor > R$ 1.000 + Aprovado
    pendente --> rejeitado : Valor > R$ 1.000 + Rejeitado
    aprovado --> processando : Iniciar processamento
    processando --> concluido : Sucesso (1ª ou 2ª tentativa)
    processando --> erro : Falha após 2 tentativas
    erro --> processando : Reprocessamento manual
    concluido --> [*]
    rejeitado --> [*]
    
    note right of pendente
        Status inicial de todos os estornos
    end note
    
    note right of aprovado
        Apenas estornos > R$ 1.000
        que foram aprovados
    end note
    
    note right of erro
        Pode ser reprocessado
        manualmente pelo usuário
    end note
```

## 🎛️ Menu Interativo - Estrutura de Navegação

```mermaid
flowchart TD
    A[Menu Principal] --> B[1. 💰 Criar Novo Estorno]
    A --> C[2. ✅ Aprovar Estorno]
    A --> D[3. ❌ Rejeitar Estorno]
    A --> E[4. 📋 Listar Estornos]
    A --> F[5. 🔄 Reprocessar Estorno]
    A --> G[6. 📊 Ver Estatísticas]
    A --> H[7. 💾 Salvar em Arquivo]
    A --> I[8. 🧪 Demonstração]
    A --> J[9. 🚪 Sair]
    
    B --> B1[Input: Valor, Cliente, Motivo]
    B1 --> B2[Validação e Criação]
    B2 --> A
    
    C --> C1[Listar Estornos Pendentes]
    C1 --> C2[Input: ID Estorno + Aprovador]
    C2 --> C3[Processar Aprovação]
    C3 --> A
    
    D --> D1[Input: ID Estorno + Aprovador]
    D1 --> D2[Processar Rejeição]
    D2 --> A
    
    E --> E1[Input: Filtro Opcional]
    E1 --> E2[Exibir Lista Filtrada]
    E2 --> A
    
    F --> F1[Input: ID Estorno com Erro]
    F1 --> F2[Reprocessar]
    F2 --> A
    
    G --> G1[Calcular e Exibir Stats]
    G1 --> A
    
    H --> H1[Gerar Arquivo JSON]
    H1 --> A
    
    I --> I1[Executar Demo Automática]
    I1 --> A
    
    J --> K[Encerrar Sistema]
    
    style A fill:#e1f5fe
    style K fill:#ffebee
```

## 🔄 Fluxo de Demonstração Automática

```mermaid
sequenceDiagram
    participant U as Usuário
    participant S as Sistema
    participant E as Estorno
    
    U->>S: Escolher opção 8 (Demo)
    S->>E: Criar estorno R$ 500 (baixo valor)
    E->>S: Processar automaticamente
    S->>E: Status: concluido
    
    S->>E: Criar estorno R$ 1500 (alto valor)
    E->>S: Status: pendente (aguarda aprovação)
    S->>E: Aprovar estorno
    E->>S: Status: aprovado → processando
    S->>E: Simular processamento com retry
    E->>S: Status: concluido
    
    S->>U: Exibir lista de estornos
    S->>U: Exibir estatísticas
    S->>U: Demo concluída
```
