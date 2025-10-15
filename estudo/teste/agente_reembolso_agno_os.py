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
  

    resultado = f"""Cálculo de Reembolso

Valor original: R$ {valor}
Imposto (15%): R$ {imposto}
Valor final do reembolso: R$ {valor_final}"""
    
    if precisa_aprovacao:
        resultado += f"\nATENÇÃO: Valor acima de R$ {teto} - Precisa aprovação do Financeiro!"
    else:
        resultado += f"\nReembolso aprovado automaticamente (abaixo de R$ {teto})."
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
    - Sistema de memória integrado
    """
    # Cria o agente (o banco de dados já está configurado no agente)
    agente = criar_agente()
    
    # Configura o AgentOS (nova API sem parâmetro db)
    agent_os = AgentOS(
        id="reembolso-agentos",
        description="Sistema de reembolso com IA",
        agents=[agente],
    )
    
    print("AgentOS configurado com sucesso!")
    return agent_os


if __name__ == "__main__":
    """
    Executa o agente usando AgentOS para produção
    """
    try:
        print("Iniciando AgentOS para aplicação web...")
        agent_os = criar_agno_os()
        
        print("Servidor web iniciado!")
        print("Acesse: http://localhost:8000")
        print("Documentação: http://localhost:8000/docs")
        
        # Obtém a aplicação FastAPI
        app = agent_os.get_app()
        
        # Inicia o servidor usando uvicorn
        import uvicorn
        uvicorn.run(app, host="0.0.0.0", port=8000)
        
    except Exception as e:
        print(f"Erro ao executar AgentOS: {e}")
