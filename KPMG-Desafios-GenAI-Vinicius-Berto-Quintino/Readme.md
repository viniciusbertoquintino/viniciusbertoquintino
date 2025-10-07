# 🚀 Desafios GenAI - Vinicius Berto Quintino

> Coleção de projetos demonstrando diferentes aplicações de Inteligência Artificial Generativa

## 📋 Visão Geral

Este repositório contém três projetos distintos que exploram diferentes aspectos da IA Generativa, desde agentes conversacionais com memória até sistemas multi-agentes e simulação de fluxos de negócio.

## 🎯 Projetos Incluídos

### [A1 - Agente de Reembolso com Memória](./A1/) 💰
**Assistente inteligente de políticas de reembolso usando RAG, Azure OpenAI e Sistema de Memória**

- ✅ **RAG (Retrieval Augmented Generation)** com base de conhecimento em PDF
- ✅ **Sistema de Memória** (curto prazo + sessão completa)
- ✅ **Interface dupla**: CLI e Web (Streamlit)
- ✅ **Cálculo automático** de reembolsos com regras de negócio
- ✅ **Exportação** de conversas em JSON

**Tecnologias**: Agno Framework, Azure OpenAI, LanceDB, Streamlit

---

### [A2 - Sistema Multi-Agentes](./A2/) 🤖
**Sistema colaborativo com 3 agentes: Redator → Crítico → Editor**

- ✅ **3 Agentes especializados** trabalhando em sequência
- ✅ **Fluxo controlado** com máximo 2 rodadas
- ✅ **Críticas com fonte** (DoD - Definition of Done)
- ✅ **Produção de comunicados** claros sobre reembolsos
- ✅ **Regras de parada** para evitar loops infinitos

**Tecnologias**: Agno Framework, Azure OpenAI

---

### [A3 - Sistema de Estorno](./A3/) 🔄
**Simulação de fluxo de estornos com regras de negócio e tratamento de erros**

- ✅ **Aprovação condicional** para valores > R$ 1.000
- ✅ **Retry automático** com até 2 tentativas
- ✅ **Dead Letter Queue (DLQ)** para reprocessamento
- ✅ **Idempotência** por request_id
- ✅ **Exportação** de dados em JSON

**Tecnologias**: Python puro (bibliotecas padrão)

---

## 🛠️ Tecnologias Utilizadas

### Frameworks e Bibliotecas
- **[Agno](https://github.com/agno-agi/agno)** - Framework de agentes IA
- **Azure OpenAI** - Modelos GPT-4 e Embeddings
- **Streamlit** - Interface web interativa
- **LanceDB** - Vector database para RAG
- **PyPDF** - Processamento de documentos PDF

### Conceitos de IA
- **RAG (Retrieval Augmented Generation)**
- **Sistema de Memória** para agentes conversacionais
- **Multi-Agentes** com orquestração
- **Vector Search** e embeddings
- **Prompt Engineering**

## 🚀 Como Executar

### Pré-requisitos
- Python 3.8+
- Conta Azure OpenAI (para A1 e A2)
- Arquivo `.env` com credenciais (veja exemplos em cada projeto)

## 📊 Demonstrações

### A1 - Agente com Memória
```bash
Você: "Qual o prazo para reembolso?"
Bot: "O prazo é de 30 dias após a compra."

Você: "E qual era o prazo mesmo?"
Bot: "Como mencionei, 30 dias após a compra." ✅ LEMBROU!
```

### A2 - Multi-Agentes
```
🚀 INICIANDO SISTEMA MULTI-AGENTES
📝 ETAPA 1: Redator escrevendo comunicado...
🔍 ETAPA 2: Crítico analisando...
❌ Problema: Prazo não especificado claramente
✍️ ETAPA 3: Editor produzindo versão final...
✅ SISTEMA CONCLUÍDO COM SUCESSO!
```

### A3 - Sistema de Estorno
```
[CRIADO] REQ_A1B2C3 - R$ 1.500,00
[APROVACAO] Valor > R$ 1000, precisa de aprovação
[APROVADO] REQ_A1B2C3 por Financeiro
[PROCESSANDO] REQ_A1B2C3...
[SUCESSO] REQ_A1B2C3 processado!
```

## 🎓 Conceitos Demonstrados

### 1. **RAG (Retrieval Augmented Generation)**
- Busca semântica em documentos
- Contexto relevante para respostas precisas
- Base de conhecimento estruturada

### 2. **Sistema de Memória para Agentes**
- Memória de curto prazo (buffer)
- Memória de sessão (persistente)
- Contexto conversacional

### 3. **Multi-Agentes**
- Divisão de responsabilidades
- Orquestração de fluxos
- Comunicação entre agentes

### 4. **Tratamento de Erros e Resiliência**
- Retry automático
- Dead Letter Queue
- Idempotência

## 📁 Estrutura do Projeto

```
Desafios---GenAI---Vinicius-Berto-Quintino/
├── A1/                          # Agente de Reembolso
│   ├── agente_reembolso.py      # Agente principal
│   ├── memoria.py               # Sistema de memória
│   ├── app.py                   # Interface Streamlit
│   ├── politica_reembolso_v1.0.pdf
│   └── README.md
├── A2/                          # Sistema Multi-Agentes
│   ├── multiagente.py           # Sistema principal
│   ├── Exemplo - ponto de partida.py
│   └── README.md
├── A3/                          # Sistema de Estorno
│   ├── estorno.py               # Lógica principal
│   ├── DIAGRAMAS.md
│   └── README.md
└── readme.md                    # Este arquivo
```

## 🎯 Objetivos dos Projetos

### A1 - Demonstração de RAG + Memória
- Como implementar busca semântica
- Sistema de memória para agentes conversacionais
- Interface dupla (CLI + Web)

### A2 - Demonstração de Multi-Agentes
- Orquestração de múltiplos agentes
- Fluxo controlado com regras de parada
- Divisão de responsabilidades

### A3 - Demonstração de Fluxo de Negócio
- Regras de negócio complexas
- Tratamento de erros e resiliência
- Simulação de sistemas reais

## 🚀 Próximos Passos

### Melhorias Sugeridas
- [ ] Interface web unificada para todos os projetos
- [ ] Métricas e analytics
- [ ] Testes automatizados
- [ ] CI/CD pipeline
- [ ] Documentação de API
- [ ] Deploy em cloud

### Expansões Possíveis
- [ ] Integração com bancos de dados reais
- [ ] Sistema de autenticação
- [ ] Logs estruturados
- [ ] Monitoramento e alertas
- [ ] Versionamento de modelos

## 📚 Recursos Adicionais

### Documentação
- [Agno Framework](https://github.com/agno-agi/agno)
- [Streamlit](https://docs.streamlit.io/)

### Conceitos de IA
- [RAG Pattern](https://docs.microsoft.com/en-us/azure/architecture/ai-ml/architecture/rag-pattern)
- [Multi-Agent Systems](https://en.wikipedia.org/wiki/Multi-agent_system)
- [Vector Databases](https://www.pinecone.io/learn/vector-database/)

## 👨‍💻 Autor

**Vinicius Berto Quintino**
- Desenvolvedor especializado em IA Generativa
- Experiência em sistemas multi-agentes e RAG
- Foco em soluções práticas e escaláveis

---

## 📄 Licença

Este projeto é para fins educacionais e demonstrativos. Consulte os arquivos individuais de cada projeto para informações específicas de licenciamento.

---

**Desenvolvido com ❤️ e muito ☕ usando Python + IA Generativa**
