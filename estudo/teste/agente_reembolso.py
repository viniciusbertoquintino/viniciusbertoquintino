import os
import sys
import asyncio
from dotenv import load_dotenv

load_dotenv()

from agno.agent import Agent
from agno.tools import tool
from agno.models.azure.openai_chat import AzureOpenAI
from agno.knowledge.embedder.azure_openai import AzureOpenAIEmbedder
#from agno.knowledge.embedder.sentence_transformer import SentenceTransformerEmbedder
from agno.knowledge.reader.pdf_reader import PDFReader
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.lancedb import LanceDb, SearchType
from agno.db.sqlite.sqlite import SqliteDb
from agno.db.postgres import PostgresDb

# Sistema de memória integrado com Agno
from agno.memory import MemoryManager, UserMemory
from agno.db.base import BaseDb

# AgnoOS para produção
from agno.os import AgentOS


# Ferramenta de Cálculo de Reembolso
@tool(stop_after_tool_call=False)
def compute_refund(valor: float):
    """
    Calcula o reembolso considerando imposto e teto máximo, recebe um valor e retorna o resultado do cálculo.
    """
    percentual_imposto: float = 15.0
    teto: float = 1000.0

    imposto = valor * (percentual_imposto / 100)
    valor_final = valor - imposto

    precisa_aprovacao = valor_final > teto
  

    resultado = f"""💰 Cálculo de Reembolso

Valor original: R$ {valor}
Imposto (15%): R$ {imposto}
Valor final do reembolso: R$ {valor_final}"""
    
    if precisa_aprovacao:
        resultado += f"\n⚠️ ATENÇÃO: Valor acima de R$ {teto} - Precisa aprovação do Financeiro!"
    else:
        resultado += f"\n✅ Reembolso aprovado automaticamente (abaixo de R$ {teto})."
    return resultado



# (Opcional) Ler TXT para usos auxiliares

def carregar_politica():
    try:
        with open("politica_reembolso_v1.0.txt", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "Erro: Arquivo de política não encontrado."



# Função para carregar Knowledge Base

async def load_knowledge_base(kb: Knowledge):
    """
    Carrega o conteúdo na Knowledge Base de forma assíncrona.
    """
    try:
        await kb.add_content_async(
            name="politica_reembolso",
            path="politica_reembolso_v1.0.pdf",   
           
        )
        print("Knowledge Base carregada com sucesso!")
    except Exception as e:
        print(f"Erro ao carregar Knowledge Base: {e}")



# Sistema de Memória Simples

def criar_memoria():
    """
    Cria o sistema de memória do agente.
    Bem simples - só configura a memória do usuário.
    """
    # 1) Banco de dados para memórias
    memory_db = SqliteDb(db_file="../tmp/agent_data.db")
    
    # 2) Sistema de memória
    memory_manager = MemoryManager(
        db=memory_db,
        memory_capture_instructions="""
        Colete informações importantes sobre o usuário:
        - Nome e dados pessoais
        - Solicitações de reembolso feitas
        - Valores e tipos de despesas
        - Preferências e histórico
        """,
        model=AzureOpenAI( 
            azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"), 
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"), 
            api_key=os.getenv("AZURE_OPENAI_API_KEY"), 
            api_version=os.getenv("AZURE_OPENAI_API_VERSION")
        )
    )
    
    print("Sistema de memória criado!")
    return memory_manager



# Agente com Knowledge (RAG) + Memória

def criar_agente():
    """
    Cria um Agent do Agno com:
      - Knowledge (RAG) em cima de arquivo PDF
      - Sistema de memória integrado
      - Modelo Azure OpenAI (chat)
      - Ferramenta compute_refund
    """

    # 1) Knowledge (LanceDB + Azure Embedder)
    embedding_provider = AzureOpenAIEmbedder(
    azure_deployment="text-embedding-3-large",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
    )
    # embedding_provider = SentenceTransformerEmbedder(726, "	PORTULAN/albertina-100m-portuguese-ptbr-encoder")

    kb = Knowledge(
        vector_db=LanceDb(
            table_name="reembolso_kb",
            uri="../tmp/lancedb",
            search_type=SearchType.hybrid,
            embedder=embedding_provider
        ),
        max_results=2,
    )

    # 2) Carrega conteúdo na Knowledge Base (assíncrono) carrega somente uma vez na inicialização
    asyncio.run(load_knowledge_base(kb))
    
    # 3) Banco de dados para o agente
    db = SqliteDb(db_file="../tmp/agent_data.db")

    # 4) Sistema de memória
    memory_manager = criar_memoria()

    # 5) Modelo de chat
    chat_model = AzureOpenAI(
        temperature=0.3, 
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"), 
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"), 
        api_key=os.getenv("AZURE_OPENAI_API_KEY"), 
        api_version=os.getenv("AZURE_OPENAI_API_VERSION")
    )

    # 6) Instruções
    instructions = """
    Você é um assistente de políticas de reembolso.
    Regras:
    - Responda com base nos trechos da base de conhecimento (RAG).
    - Use suas memórias sobre o usuário para personalizar respostas.
    - Se precisar calcular, use a ferramenta compute_refund.
    - Seja claro e educado nas respostas.
    """

    # 7) Cria o Agent com RAG + Memória
    agente = Agent(
        model=chat_model,
        name="Assistente de Reembolso",
        instructions=instructions,
        db=db,
        memory_manager=memory_manager,     # Sistema de memória integrado
        
        # RAG
        knowledge=kb,
        search_knowledge=True,
        add_knowledge_to_context=True,

        # Ferramentas
        tools=[compute_refund],

        # Configurações de memória
        enable_user_memories=True,         # Ativa memórias do usuário
        enable_session_summaries=True,     # Ativa resumos de sessão
        add_history_to_context=True,      # Adiciona histórico às mensagens
        #add_history_to_context_max_responses=10,           # Últimas 10 respostas no contexto

        markdown=True,
    )
    return agente


def criar_agno_os():
    """
    Cria o AgentOS para produção com:
    - Agente de reembolso configurado
    - Banco de dados PostgreSQL (produção) ou SQLite (desenvolvimento)
    - Sistema de memória integrado
    """
    # Configuração do banco de dados
    # Em produção, usar PostgreSQL; em desenvolvimento, SQLite
    if os.getenv("DATABASE_URL"):
        db = PostgresDb(db_url=os.getenv("DATABASE_URL"))
        print("🗄️ Usando PostgreSQL para produção")
    else:
        db = SqliteDb(db_file="../tmp/agent_data.db")
        print("🗄️ Usando SQLite para desenvolvimento")
    
    # Cria o agente
    agente = criar_agente()
    
    # Configura o AgentOS
    agent_os = AgentOS(
        agents=[agente],
        db=db,
        show_tool_calls=False,  # Desabilita logs de ferramentas em produção
        debug_mode=False,       # Desabilita modo debug em produção
    )
    
    print("🚀 AgentOS configurado com sucesso!")
    return agent_os


def processar_pergunta(agente, pergunta: str, user_id: str = "usuario_padrao"):
    
    try:
        
        resposta = agente.run(pergunta, user_id=user_id)
        texto_resposta = getattr(resposta, "content", str(resposta)) # (getattr) atributo de um objeto, nesse caso Retorna o texto da resposta ou a resposta completa / # Em prod usar o Try Except para retornar o texto da resposta ou a resposta completa (mais seguro)
        
        
        return texto_resposta
        
    except Exception as e:
        return f"❌ Erro ao processar pergunta: {e}"


def mostrar_memorias_usuario(agente, user_id: str = "usuario_padrao"):
    
    # Mostra as memórias do usuário de forma simples.
   
    try:
        memorias = agente.memory_manager.get_user_memories(user_id=user_id)
        
        print(f"\n🧠 **Memórias do usuário {user_id}:**")
        if memorias:
            for i, memoria in enumerate(memorias, 1):
                print(f"   {i}. {memoria}")
        else:
            print("   Nenhuma memória encontrada.")
            
    except Exception as e:
        print(f"❌ Erro ao mostrar memórias: {e}")


def mostrar_estatisticas(agente, user_id: str = "usuario_padrao"):
    
    # Mostra estatísticas simples do sistema.
    
    try:
        print("\n📊 **Estatísticas do Sistema:**")
        
        # Memórias do usuário
        memorias = agente.memory_manager.get_user_memories(user_id=user_id)
        print(f"   • Memórias do usuário: {len(memorias)}")
        
        # Histórico da sessão
        mensagens = agente.get_messages_for_session()
        print(f"   • Mensagens na sessão: {len(mensagens)}")
        
    except Exception as e:
        print(f"❌ Erro ao mostrar estatísticas: {e}")


def executar_modo_console():
    """
    Executa o agente em modo console (desenvolvimento/teste)
    """
    try:
        print("🚀 Iniciando agente de reembolso com memória integrada...")
        agente = criar_agente()
        
        # ID do usuário (pode ser personalizado)
        user_id = "usuario_padrao"
        print(f"👤 Usuário: {user_id}")
        print("\n" + "=" * 50)
        print("💡 Comandos especiais:")
        print("   • 'memorias' - Ver memórias do usuário")
        print("   • 'stats' - Ver estatísticas")
        print("   • 'teste' - Modo teste automático")
        print("   • 'sair' - Sair do programa")
        print("=" * 50 + "\n")

        while True:
            pergunta = input("💬 Digite uma pergunta: ")
            
            # Comandos especiais
            if pergunta == "exit" or pergunta == "sair":
                print("👋 Saindo...")
                break
            
            if pergunta == "memorias":
                mostrar_memorias_usuario(agente, user_id)
                continue
            
            if pergunta == "stats" or pergunta == "estatisticas":
                mostrar_estatisticas(agente, user_id)
                continue

            if pergunta == "test" or pergunta == "teste":
                print("\n" + "=" * 60)
                print("💬 MODO TESTE - Conversação com memória integrada")
                print("=" * 60 + "\n")

                pergunta1 = "Olá! Meu nome é João Silva e trabalho na empresa TechCorp."
                print(f"❓ Pergunta 1: {pergunta1}")
                resposta1 = processar_pergunta(agente, pergunta1, user_id)
                print(f"🤖 Resposta: {resposta1}\n")

                pergunta2 = "Quais despesas são reembolsáveis e qual o prazo para solicitação?"
                print(f"❓ Pergunta 2: {pergunta2}")
                resposta2 = processar_pergunta(agente, pergunta2, user_id)
                print(f"🤖 Resposta: {resposta2}\n")

                pergunta3 = "Calcule o reembolso de R$ 1.250,00"
                print(f"❓ Pergunta 3: {pergunta3}")
                resposta3 = processar_pergunta(agente, pergunta3, user_id)
                print(f"🤖 Resposta: {resposta3}\n")
                
                pergunta4 = "Qual é o meu nome mesmo?"  # Testa a memória!
                print(f"❓ Pergunta 4 (testando memória): {pergunta4}")
                resposta4 = processar_pergunta(agente, pergunta4, user_id)
                print(f"🤖 Resposta: {resposta4}\n")
                
                # Mostra estatísticas e memórias
                mostrar_estatisticas(agente, user_id)
                mostrar_memorias_usuario(agente, user_id)
                
                break
            
            # Processa pergunta normal com memória integrada
            resposta = processar_pergunta(agente, pergunta, user_id)
            print(f"\n🤖 Resposta: {resposta}\n")

    except Exception as e:
        print(f"❌ Erro ao executar o agente: {e}")


def executar_modo_web():
    """
    Executa o agente como aplicação web usando AgentOS
    """
    try:
        print("🌐 Iniciando AgentOS para aplicação web...")
        agent_os = criar_agno_os()
        
        # Obtém a aplicação FastAPI
        app = agent_os.get_app()
        
        print("🚀 Servidor web iniciado!")
        print("📡 Acesse: http://localhost:8000")
        print("📚 Documentação: http://localhost:8000/docs")
        
        # Inicia o servidor (em produção, usar uvicorn diretamente)
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=8000)
        
    except Exception as e:
        print(f"❌ Erro ao executar AgentOS: {e}")


if __name__ == "__main__":
    import sys
    
    # Verifica se deve executar em modo web ou console
    if len(sys.argv) > 1 and sys.argv[1] == "--web":
        executar_modo_web()
    else:
        print("💡 Para executar em modo web, use: python agente_reembolso.py --web")
        print("🖥️ Executando em modo console...\n")
        executar_modo_console()
