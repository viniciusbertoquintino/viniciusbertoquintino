# 💰 Agente de Reembolso com Memória Integrada

> Assistente inteligente de políticas de reembolso usando RAG, Sistema de Memória.

## 🎯 O que é este projeto?

Um agente conversacional que:

- ✅ Responde perguntas sobre política de reembolso
- ✅ Calcula valores de reembolso automaticamente
- ✅ Usa RAG (Retrieval Augmented Generation) com base de conhecimento
- ✅ Memoria Integrada (Memorias do Usuário e de Sessão)
- ✅ Interface CLI e Web (Streamlit)

## 🧠 Sistema de Memória Integrado

### Diferenciais:

1. **Memórias do Usuário**

   - Aprende sobre preferências e dados pessoais
   - Busca semântica inteligente
   - Persistência automática em SQLite
2. **Histórico de Sessões**

   - Todas as conversas salvas automaticamente
   - Consulta por sessão ou usuário
   - Backup automático
3. **Resumos de Sessão**

   - Contexto condensado de conversas longas
   - Geração automática de resumos
   - Mantém informações importantes

### Exemplo:

```text
Você: "Olá! Meu nome é João Silva e trabalho na TechCorp."
Bot: "Olá João! Como posso ajudá-lo com reembolsos?"

Você: "Qual é o meu nome mesmo?" 
Bot: "Seu nome é João Silva, da empresa TechCorp." ✅ LEMBROU!
```

## 🚀 Início Rápido

### 1. Instalação

```bash
# Clone ou entre no diretório
cd a1

# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente

# Edite o .env com suas credenciais Azure OpenAI
```

### 2. Execute

**Terminal (CLI):**

```bash
python agente_reembolso.py
```

**Interface Web:**

```bash
streamlit run app.py
```

## 🎓 Tutoriais Práticos

## 🛠️ Arquitetura

```text
┌─────────────┐
│  Usuário    │
└──────┬──────┘
       │
       ↓
┌──────────────────┐
│  Interface       │ ← CLI ou Streamlit
│  (app.py)        │
└────────┬─────────┘
         │
         ↓
┌─────────────────────────────┐
│      Agente (Agno)          │
│                             │
│  ┌─────────────────────────┐│
│  │    Sistema de Memória   ││ ← Integrado!
│  │                         ││
│  │  • Memórias do Usuário  ││
│  │  • Histórico Sessões    ││
│  │  • Resumos Automáticos  ││
│  └─────────────────────────┘│
│                             │
│  ┌─────────────────────────┐│
│  │         RAG             ││
│  │                         ││
│  │  • Knowledge Base       ││
│  │  • Vector DB (LanceDB)  ││
│  │  • Azure Embeddings     ││
│  └─────────────────────────┘│
│                             │
│  ┌─────────────────────────┐│
│  │         LLM             ││
│  │                         ││
│  │  • Azure OpenAI (GPT-4) ││
│  │  • Ferramentas          ││
│  └─────────────────────────┘│
└─────────────────────────────┘
```

## 📦 Estrutura de Arquivos

```text
final/
├── agente_reembolso.py          # Agente principal com memória integrada
├── app.py                        # Interface Streamlit
├── requirements.txt              # Dependências
├── politica_reembolso_v1.0.pdf   # Base de conhecimento
├── politica_reembolso_v1.0.txt   # Base de conhecimento (Fallback)
├── README.md                     # Este arquivo
└── tmp/                         # Dados temporários (SQLite, LanceDB)
    ├── agent_data.db            # Banco de dados do agente
    └── lancedb/                 # Vector database
```

## 💡 Funcionalidades

### 1. RAG (Retrieval Augmented Generation)

- Base de conhecimento em PDF
- Busca semântica com embeddings
- Vector DB (LanceDB)

### 2. Ferramentas (Tools)

- `compute_refund()`: Calcula reembolso com impostos e teto

### 3. Memória Integrada

- **Memórias do usuário**: Aprende preferências e dados pessoais
- **Histórico de sessões**: Todas as conversas salvas automaticamente
- **Resumos automáticos**: Contexto condensado de conversas longas
- **Persistência robusta**: SQLite com backup automático

### 4. Interface

- CLI interativo
- Web app com Streamlit (versão simplificada)
- Tratamento automático de respostas

### 5. Tratamento de Respostas

- **Formatação automática**: Adiciona emojis e destaca valores
- **Personalização**: Mensagens de erro customizadas
- **Melhoria visual**: Quebras de linha e formatação markdown
- **Flexibilidade**: Fácil de personalizar para suas necessidades

## 🎮 Comandos Disponíveis

### Terminal:

| Comando      | Ação                          |
| ------------ | ------------------------------- |
| `teste`    | Executa teste automático       |
| `memorias` | Mostra memórias do usuário    |
| `stats`    | Mostra estatísticas do sistema |
| `sair`     | Sai do programa                 |

### Streamlit:

- 🗑️ Limpar conversa
- 🎨 Tratamento automático de respostas
- 💡 Interface simplificada

## 🧪 Testes

```bash
# Teste completo do agente
python agente_reembolso.py
> teste
```

## 🔧 Personalização

### Mudar configurações de memória:

```python
# Em agente_reembolso.py, linha 194-197:
enable_user_memories=True,         # Ativa memórias do usuário
enable_session_summaries=True,     # Ativa resumos de sessão
add_history_to_messages=True,      # Adiciona histórico às mensagens
num_history_responses=5,           # Últimas 5 respostas no contexto
```

### Mudar temperatura do modelo:

```python
# Em agente_reembolso.py, linha 159:
chat_model = AzureOpenAI(
    temperature=0.3,  # ← Ajuste aqui (0.0 = mais determinístico, 1.0 = mais criativo)
    ...
)
```

### Personalizar instruções de memória:

```python
# Em agente_reembolso.py, linha 101-107:
memory_capture_instructions="""
Colete informações importantes sobre o usuário:
- Nome e dados pessoais
- Solicitações de reembolso feitas
- Valores e tipos de despesas
- Preferências e histórico
"""
```

### Personalizar tratamento de respostas:

```python
# Em app.py, função tratar_resposta():
def tratar_resposta(resposta):
    texto = str(resposta)
    
    # Adicionar emojis personalizados
    if "reembolso" in texto.lower():
        texto = "💰 " + texto
    
    # Destacar valores em dinheiro
    texto = re.sub(r'R\$\s*(\d+)', r'**R$ \1**', texto)
    
    # Adicionar data/hora
    from datetime import datetime
    texto += f"\n\n*Resposta gerada em: {datetime.now().strftime('%H:%M')}*"
    
    return texto
```

## 📊 Exemplos de Uso

### Exemplo 1: Pergunta sobre política

```text
Você: "Devolução por arrependimento?"

Bot: "A política de reembolso para devolução por arrependimento estabelece que o prazo máximo para solicitar a devolução é de 7 dias a partir da data de recebimento do produto. O cliente deve preencher o formulário de reembolso no site e, após receber a confirmação do recebimento por e-mail, aguardar até 3 dias para a confirmação da possibilidade de reembolso. Após a confirmação, o reembolso será realizado em até 5 dias úteis via PIX. 😊"
```

### Exemplo 2: Cálculo de reembolso

```text
Você: "Calcule o reembolso de R$ 1.250,00"

Bot: "
💰 Cálculo de Reembolso
Valor original: R$ 1250.0
Imposto (15%): R$ 187.5
Valor final: R$ 1062.5
⚠️ ATENÇÃO: Valor acima de R$ 1000.0 - Precisa aprovação do Financeiro!
"
```

### Exemplo 3: Memória integrada

```text
Você: "Olá! Meu nome é João Silva e trabalho na TechCorp."
Bot: "Olá João! Como posso ajudá-lo com reembolsos na TechCorp?"

Você: "Qual é o meu nome mesmo?"
Bot: "Seu nome é João Silva, da empresa TechCorp." ✅ LEMBROU!

Você: "Calcule o reembolso de R$ 1.250,00"
Bot: "💰 Cálculo de Reembolso para João Silva..."

Você: "Qual era o valor que calculei?"
Bot: "Você solicitou o cálculo para R$ 1.250,00..." ✅ LEMBROU!
```

## 🔍 Tecnologias Utilizadas

- **Framework**: [Agno](https://github.com/agno-agi/agno) - Framework de agentes IA
- **LLM**: Azure OpenAI (GPT-4)
- **Vector DB**: LanceDB
- **Embeddings**: Azure OpenAI Embeddings
- **Interface**: Streamlit
- **PDF Reader**: PyPDF.

## 🎉 Contribuindo

Melhorias são bem-vindas! Algumas ideias:

- [X] ~~Busca semântica na memória de sessão~~ ✅ **Implementado!**
- [X] ~~Resumo automático de conversas longas~~ ✅ **Implementado!**
- [ ] Categorização de perguntas
- [ ] Feedback do usuário
- [ ] Testes unitários
- [ ] CI/CD
- [ ] Interface web melhorada
- [ ] Suporte a múltiplos usuários

## 🔄 Mudanças Recentes

### V2.1 - Interface Simplificada

- ✅ **Interface Streamlit simplificada** - Removidas complexidades desnecessárias
- ✅ **Tratamento automático de respostas** - Formatação inteligente antes de exibir
- ✅ **Código mais limpo** - Foco na funcionalidade essencial

### V2.0 - Memória Integrada com Agno

- ✅ **Removida dependência** do arquivo `memoria.py`
- ✅ **Sistema de memória integrado** diretamente no Agno
- ✅ **3 tipos de memória**: Usuário, Sessão e Resumos
- ✅ **Persistência robusta** em SQLite
- ✅ **Código 5x mais simples** (30 vs. 169 linhas)
- ✅ **Funcionalidades automáticas** sem configuração manual

---

**Desenvolvido por Vinicius com bastante dedicação. Foram exploradas diferentes abordagens de IA para mostrar que não existe uma solução única — tudo depende do contexto específico de cada problema.**
