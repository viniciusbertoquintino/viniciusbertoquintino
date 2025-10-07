# 💰 Agente de Reembolso com Memória V2

> Assistente inteligente de políticas de reembolso usando RAG, Azure OpenAI e Sistema de Memória

## 🎯 O que é este projeto?

Um agente conversacional que:

- ✅ Responde perguntas sobre política de reembolso
- ✅ Calcula valores de reembolso automaticamente
- ✅ Usa RAG (Retrieval Augmented Generation) com base de conhecimento
- ✅ **TEM MEMÓRIA!** Lembra das conversas anteriores
- ✅ Interface CLI e Web (Streamlit)

## 🧠 Sistema de Memória

### Diferenciais:

1. **Memória de Curto Prazo (Buffer)**

   - Guarda as últimas 10 mensagens
   - Contexto rápido para o agente
   - Eficiente e econômico
2. **Memória de Sessão**

   - Histórico completo da conversa
   - Exportável em JSON
   - Persistente entre execuções

### Exemplo:

```
Você: "Qual o prazo para reembolso?"
Bot: "O prazo é de 30 dias após a compra."

Você: "E qual era o prazo mesmo?" 
Bot: "Como mencionei, 30 dias após a compra." ✅ LEMBROU!
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

|  |  |
| - | - |
|  |  |

## 🎓 Tutoriais Práticos

## 🛠️ Arquitetura

```
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
    ┌────┴────┐
    ↓         ↓
┌────────┐ ┌──────────────┐
│Memória │ │   Agente     │
│        │ │   (Agno)     │
│Buffer  │ │              │
│Sessão  │ │   ┌────────┐ │
└────────┘ │   │  RAG   │ │
           │   │  KB    │ │
           │   │  LLM   │ │
           │   └────────┘ │
           └──────────────┘
```

## 📦 Estrutura de Arquivos

```
a1/
├── agente_reembolso.py          # Agente principal com memória
├── memoria.py                    # Sistema de memória
├── app.py                        # Interface Streamlit
├── requirements.txt              # Dependências
├── politica_reembolso_v1.0.pdf   # Base de conhecimento
├── politica_reembolso_v1.0.txt   # Base de conhecimento (Fallback)
├── README.md                     # Este arquivo
```

## 💡 Funcionalidades

### 1. RAG (Retrieval Augmented Generation)

- Base de conhecimento em PDF
- Busca semântica com embeddings
- Vector DB (LanceDB)

### 2. Ferramentas (Tools)

- `compute_refund()`: Calcula reembolso com impostos e teto

### 3. Memória

- Buffer de curto prazo (10 mensagens)
- Sessão completa (ilimitada)
- Exportação em JSON

### 4. Interface

- CLI interativo
- Web app com Streamlit
- Estatísticas em tempo real

## 🎮 Comandos Disponíveis

### Terminal:

| Comando    | Ação                           |
| ---------- | -------------------------------- |
| `teste`  | Executa teste automático        |
| `stats`  | Mostra estatísticas da memória |
| `limpar` | Reseta memória                  |
| `sair`   | Sai e salva sessão              |

### Streamlit:

- 📊 Estatísticas na sidebar
- 🗑️ Limpar conversa
- 📥 Baixar sessão (JSON)

## 🧪 Testes

```bash
# Teste completo do agente
python agente_reembolso.py
> teste
```

## 🔧 Personalização

### Mudar tamanho do buffer:

```python
# Em agente_reembolso.py, linha 206:
memoria = MemoriaAgente(limite_curto_prazo=10)  # Padrão

# Altere para:
memoria = MemoriaAgente(limite_curto_prazo=15)  # Maior (podendo ser um valor maior)
```

### Mudar temperatura do modelo:

```python
# Em agente_reembolso.py, linha 120:
chat_model = AzureOpenAI(
    temperature=0.3,  # ← Ajuste aqui (0.0 = mais determinístico, 1.0 = mais criativo)
    ...
)
```

## 📊 Exemplos de Uso

### Exemplo 1: Pergunta sobre política

```
Você: "Devolução por arrependimento?"

Bot: "A política de reembolso para devolução por arrependimento estabelece que o prazo máximo para solicitar a devolução é de 7 dias a partir da data de recebimento do produto. O cliente deve preencher o formulário de reembolso no site e, após receber a confirmação do recebimento por e-mail, aguardar até 3 dias para a confirmação da possibilidade de reembolso. Após a confirmação, o reembolso será realizado em até 5 dias úteis via PIX. 😊"
```

### Exemplo 2: Cálculo de reembolso

```
Você: "Calcule o reembolso de R$ 1.250,00"

Bot: "
💰 Cálculo de Reembolso
Valor original: R$ 1250.0
Imposto (15%): R$ 187.5
Valor final: R$ 1062.5
⚠️ ATENÇÃO: Valor acima de R$ 1000.0 - Precisa aprovação do Financeiro!
"
```

### Exemplo 3: Memória contextual

```
Você: "Qual o prazo para reembolso?"
Bot: "30 dias após a compra."

Você: "E se passar desse prazo?"
Bot: "Caso ultrapasse os 30 dias mencionados anteriormente..." ✅
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

- [ ] Busca semântica na memória de sessão
- [ ] Resumo automático de conversas longas
- [ ] Categorização de perguntas
- [ ] Feedback do usuário
- [ ] Testes unitários
- [ ] CI/CD

---

**Desenvolvido com bastante dedicação, algumas madrugadas viradas e muito café (risos). Foram exploradas diferentes abordagens de IA para mostrar que não existe uma solução única — tudo depende do contexto específico de cada problema.**
