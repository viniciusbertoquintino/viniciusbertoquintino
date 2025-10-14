# 🧳 Assistente de Viagens com LangChain

Um assistente inteligente de viagens construído com LangChain de forma **simples e didática**. O assistente funciona através de uma interface de chat no terminal e ajuda usuários a planejar viagens usando inteligência artificial.

## ✨ Funcionalidades

- **Chat Interativo no Terminal**: Interface conversacional simples e direta
- **Assistente Especializado**: Focado em planejamento de viagens, destinos e roteiros
- **Código Simples**: Estrutura fácil de entender para iniciantes em programação
- **Tratamento de Erros**: Mensagens amigáveis quando algo dá errado
- **Interface Visual**: Emojis e formatação para tornar a experiência mais divertida
- **Comando de Saída**: Digite 'sair', 'exit' ou 'tchau' para encerrar o programa

## 🚀 Tecnologias Utilizadas

- **Python 3.8+**: Linguagem principal
- **LangChain OpenAI**: Integração simples com modelos OpenAI
- **OpenAI GPT-4o-mini**: Modelo de linguagem (temperatura: 0.3)
- **python-dotenv**: Gerenciamento de variáveis de ambiente

> **Nota**: Esta versão foi simplificada para iniciantes, removendo dependências complexas como LangChain Core e Community.

## 📋 Pré-requisitos

- Python 3.8 ou superior
- Conta OpenAI com API key
- Conexão com a internet

## 🛠️ Instalação

1. **Clone o repositório**
   ```bash
   git clone <url-do-repositorio>
   cd "Assistente de Viagens com LangChain"
   ```

2. **Crie um ambiente virtual**
   ```bash
   python -m venv venv
   # No Windows:
   venv\Scripts\activate
   # No Linux/Mac:
   source venv/bin/activate
   ```

3. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure a API Key da OpenAI**
   
   Crie um arquivo `.env` na raiz do projeto:
   ```env
   OPENAI_API_KEY=sua_chave_openai_aqui
   ```

## 🎯 Como Usar

### Executando o Assistente

```bash
python app.py
```

### Interface do Programa

Ao executar, você verá:
```
🌟 Bem-vindo ao Assistente de Viagens! 🌟
Digite 'sair' para encerrar a conversa.

Você: 
```

### Como Interagir

1. **Digite sua pergunta** após "Você: "
2. **Pressione Enter** para enviar
3. **Aguarde a resposta** do assistente
4. **Continue a conversa** normalmente
5. **Digite 'sair', 'exit' ou 'tchau'** para encerrar

### Exemplo de Conversa

```
🌟 Bem-vindo ao Assistente de Viagens! 🌟
Digite 'sair' para encerrar a conversa.

Você: Olá, quero planejar uma viagem
🗺️ Assistente: Olá! Fico feliz em ajudar você a planejar sua viagem! Para começar, preciso de algumas informações:

1. Para onde você gostaria de viajar?
2. Com quantas pessoas você vai viajar?
3. Por quanto tempo você planeja ficar?

Com essas informações, posso criar um roteiro personalizado e dar dicas específicas para sua viagem!

Você: Quero ir para o Japão, sou eu e minha esposa, por 10 dias
🗺️ Assistente: Que viagem incrível! O Japão é um destino maravilhoso para 10 dias. Vou criar um roteiro especial para vocês dois...

Você: sair
✈️ Assistente: Até mais! Aproveite sua viagem! ✈️
```

## 📁 Estrutura do Projeto

```
Assistente de Viagens com LangChain/
├── app.py                 # Aplicação principal (54 linhas)
├── requirements.txt       # Dependências Python
├── .env                  # Variáveis de ambiente (criar)
└── README.md            # Este arquivo
```

## 🔧 Como Funciona (Análise do Código Simplificado)

### 1. **Configuração Inicial**
```python
# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Configura o modelo GPT-4o-mini com temperatura 0.3 (mais consistente)
modelo_ia = ChatOpenAI(temperature=0.3, model="gpt-4o-mini")
```

### 2. **Instruções do Assistente**
```python
# Instruções simples em português
instrucoes = """Você é um assistente de viagens amigável e útil. 
Sua função é ajudar as pessoas a planejar viagens, dando sugestões de:
- Destinos interessantes
- Roteiros de viagem
- Dicas práticas
- Onde comer e se hospedar

Seja sempre prestativo e dê conselhos úteis!"""
```

### 3. **Função Principal do Chat**
```python
def iniciar_assistente_viagem():
    # Loop principal que:
    # 1. Pede entrada do usuário
    # 2. Cria mensagem completa (instruções + pergunta)
    # 3. Envia para a IA
    # 4. Exibe resposta
    # 5. Repete até comando de saída
```

### 4. **Tratamento de Erros**
```python
try:
    # Envia pergunta para IA
    resposta = modelo_ia.invoke(mensagem_completa)
    print(f"🗺️ Assistente: {resposta.content}\n")
except Exception as erro:
    # Mostra erro amigável se algo der errado
    print(f"❌ Erro: {erro}")
```

### 5. **Fluxo Simplificado**
1. **Carrega configurações** (API key, modelo)
2. **Define instruções** do assistente
3. **Inicia loop de chat**
4. **Captura pergunta** do usuário
5. **Combina instruções + pergunta**
6. **Envia para IA** e recebe resposta
7. **Exibe resposta** formatada
8. **Repete** até comando de saída

## ⚙️ Configurações Técnicas

### Parâmetros do Modelo
- **Modelo**: `gpt-4o-mini`
- **Temperatura**: `0.3` (mais consistente e previsível)
- **Sem histórico**: Cada pergunta é independente (mais simples)

### Dependências Simplificadas
```
langchain-openai
python-dotenv
```

> **Vantagem**: Menos dependências = instalação mais rápida e menos conflitos!

## 🚨 Solução de Problemas

### Erro: "Invalid API key"
```
Error: Invalid API key
```
**Solução**: Verifique se o arquivo `.env` existe e contém:
```env
OPENAI_API_KEY=sua_chave_real_aqui
```

### Erro: "ModuleNotFoundError"
```
ModuleNotFoundError: No module named 'langchain_openai'
```
**Solução**: Execute:
```bash
pip install -r requirements.txt
```

### Erro: "Connection error"
**Solução**: Verifique sua conexão com a internet

## 🔮 Possíveis Melhorias Futuras

- [ ] Interface web com Streamlit
- [ ] Salvamento de histórico em arquivo
- [ ] Integração com APIs de clima/mapas
- [ ] Exportação de roteiros
- [ ] Suporte a múltiplos idiomas
- [ ] Adicionar mais emojis e formatação
- [ ] Sistema de favoritos para destinos

## 📊 Estatísticas do Projeto

- **Linhas de Código**: 54 linhas (simplificado!)
- **Dependências**: 2 pacotes (reduzido de 4!)
- **Tempo de Setup**: ~2 minutos (mais rápido!)
- **Modelo**: GPT-4o-mini
- **Interface**: Terminal/Console com emojis
- **Complexidade**: Iniciante-friendly
- **Temperatura**: 0.3 (mais consistente)

## 🤝 Contribuindo

1. Faça um fork do projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT.

## 👥 Autor

- **Vinicius** - *Desenvolvimento inicial*

## 🙏 Agradecimentos

- Equipe do LangChain pela documentação
- Comunidade OpenAI pelos modelos
- Contribuidores do projeto

---

⭐ **Se este projeto foi útil, considere dar uma estrela!**

## 💡 Dicas de Uso

1. **Seja específico**: "Quero ir para Tóquio" é melhor que "Quero viajar"
2. **Experimente**: Teste diferentes tipos de perguntas
3. **Salve informações**: Anote as sugestões importantes
4. **Use emojis**: O assistente responde com emojis para tornar mais divertido
5. **Pergunte sobre tudo**: Destinos, hotéis, restaurantes, transporte, etc.

## 🔍 Detalhes Técnicos

### Fluxo de Execução Simplificado
1. Carrega variáveis de ambiente
2. Configura modelo de IA
3. Define instruções do assistente
4. Inicia loop de chat
5. Captura entrada do usuário
6. Combina instruções + pergunta
7. Envia para IA e recebe resposta
8. Exibe resposta formatada
9. Repete até comando de saída

### Estrutura de Dados Simplificada
- **instrucoes**: String com as instruções do assistente
- **modelo_ia**: Instância do ChatOpenAI
- **mensagem_completa**: Combinação de instruções + pergunta do usuário
- **Sem histórico**: Cada pergunta é independente (mais simples!)