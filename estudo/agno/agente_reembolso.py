
# =============================================================================
# AGENTE DE REEMBOLSO - ESTRUTURA SIMPLES E DIDÁTICA
# =============================================================================

# Imports necessários
import os
import asyncio
from dotenv import load_dotenv

# Agno Framework
from agno.agent import Agent
from agno.tools import tool
from agno.models.azure.openai_chat import AzureOpenAI
from agno.knowledge.embedder.azure_openai import AzureOpenAIEmbedder
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.lancedb import LanceDb, SearchType
from agno.db.sqlite.sqlite import SqliteDb
from agno.memory import MemoryManager
from agno.os import AgentOS

# Carrega variáveis de ambiente
load_dotenv()

# =============================================================================
# 1. FERRAMENTA DE CÁLCULO DE REEMBOLSO
# =============================================================================

@tool(stop_after_tool_call=False)
def compute_refund(valor: float):
    """
    Calcula o reembolso considerando imposto e teto máximo.
    Recebe um valor e retorna o resultado do cálculo.
    """
    # Configurações da política
    percentual_imposto = 15.0
    teto = 1000.0

    # Cálculos
    imposto = valor * (percentual_imposto / 100)
    valor_final = valor - imposto
    precisa_aprovacao = valor_final > teto

    # Monta resultado
    resultado = f"""Cálculo de Reembolso

Valor original: R$ {valor}
Imposto (15%): R$ {imposto}
Valor final do reembolso: R$ {valor_final}"""
    
    if precisa_aprovacao:
        resultado += f"\nATENÇÃO: Valor acima de R$ {teto} - Precisa aprovação do Financeiro!"
    else:
        resultado += f"\nReembolso aprovado automaticamente (abaixo de R$ {teto})."
    
    return resultado

# =============================================================================
# 2. CONFIGURAÇÃO DA KNOWLEDGE BASE (RAG)
# =============================================================================

async def carregar_knowledge_base(kb: Knowledge):
    """
    Carrega o conteúdo na Knowledge Base de forma assíncrona.
    """
    try:
        await kb.add_content_async(
            name="politica_reembolso",
            path="politica_reembolso_v1.0.pdf"
        )
        print("✅ Knowledge Base carregada com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao carregar Knowledge Base: {e}")

def criar_knowledge_base():
    """
    Cria e configura a Knowledge Base com LanceDB e Azure Embeddings.
    """
    # Provider de embeddings
    embedding_provider = AzureOpenAIEmbedder(
        azure_deployment="text-embedding-3-large",
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
    )

    # Knowledge Base
    kb = Knowledge(
        vector_db=LanceDb(
            table_name="reembolso_kb",
            uri="../tmp/lancedb",
            search_type=SearchType.hybrid,
            embedder=embedding_provider
        ),
        max_results=2,
    )

    # Carrega conteúdo
    asyncio.run(carregar_knowledge_base(kb))
    
    return kb

# =============================================================================
# 3. SISTEMA DE MEMÓRIA
# =============================================================================

def criar_sistema_memoria():
    """
    Cria o sistema de memória do agente.
    """
    # Banco de dados para memórias
    memory_db = SqliteDb(db_file="../tmp/agent_data.db")
    
    # Sistema de memória
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
    
    print("✅ Sistema de memória criado!")
    return memory_manager

# =============================================================================
# 4. CRIAÇÃO DO AGENTE
# =============================================================================

def criar_agente():
    """
    Cria o agente principal com todas as funcionalidades:
    - Knowledge Base (RAG)
    - Sistema de memória
    - Ferramenta de cálculo
    - Modelo Azure OpenAI
    """
    
    # 1. Knowledge Base
    kb = criar_knowledge_base()
    
    # 2. Sistema de memória
    memory_manager = criar_sistema_memoria()
    
    # 3. Banco de dados do agente
    db = SqliteDb(db_file="../tmp/agent_data.db")

    # 4. Modelo de chat
    chat_model = AzureOpenAI(
        temperature=0.3, 
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"), 
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"), 
        api_key=os.getenv("AZURE_OPENAI_API_KEY"), 
        api_version=os.getenv("AZURE_OPENAI_API_VERSION")
    )

    # 5. Instruções do agente
    instructions = """
    Você é um assistente de políticas de reembolso.
    
    Regras:
    - Responda com base nos trechos da base de conhecimento (RAG)
    - Use suas memórias sobre o usuário para personalizar respostas
    - Se precisar calcular, use a ferramenta compute_refund
    - Seja claro e educado nas respostas
    """

    # 6. Cria o agente
    agente = Agent(
        
        model=chat_model,
        name="Assistente de Reembolso",
        instructions=instructions,
        db=db,
        memory_manager=memory_manager,
        
        # RAG
        knowledge=kb,
        search_knowledge=True,
        add_knowledge_to_context=True,

        # Ferramentas
        tools=[compute_refund],

        # Configurações de memória
        enable_user_memories=True,
        enable_session_summaries=True,
        add_history_to_context=True,

        markdown=True,
    )
    
    print("✅ Agente criado com sucesso!")
    return agente

# =============================================================================
# 5. AGENTOS PARA PRODUÇÃO
# =============================================================================

def criar_agno_os():
    """
    Cria o AgentOS para produção.
    """
    agente = criar_agente()
    
    agent_os = AgentOS(
        id="reembolso-agentos",
        description="Sistema de reembolso com IA",
        agents=[agente],
    )
    
    print("✅ AgentOS configurado com sucesso!")
    return agent_os

# =============================================================================
# 6. EXECUÇÃO PRINCIPAL
# =============================================================================

if __name__ == "__main__":
    """
    Executa o agente usando AgentOS para produção.
    """
    try:
        print("🚀 Iniciando AgentOS para aplicação web...")
        agent_os = criar_agno_os()
        
        print("🌐 Servidor web iniciado!")
        print("📍 Acesse: http://localhost:8000")
        print("📚 Documentação: http://localhost:8000/docs")
        
        # Obtém a aplicação FastAPI e inicia o servidor
        app = agent_os.get_app()
        agent_os.serve(app=app, reload=True)
        
    except Exception as e:
        print(f"❌ Erro ao executar AgentOS: {e}")



