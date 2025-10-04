import os
import sys
import asyncio
from dotenv import load_dotenv

# Configura encoding UTF-8 para Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

load_dotenv()

from agno.agent import Agent
from agno.tools import tool
from agno.models.azure.openai_chat import AzureOpenAI
from agno.knowledge.embedder.azure_openai import AzureOpenAIEmbedder
from agno.knowledge.reader.pdf_reader import PDFReader
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.lancedb import LanceDb
from agno.db.sqlite.sqlite import SqliteDb


# ========================================
# Ferramenta de Cálculo (com fix no ">")
# ========================================
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
  

    resultado = f"""
💰 **Cálculo de Reembolso**

    Valor original: R$ {valor}
    Imposto (15%): R$ {imposto}
    Valor final do reembolso: R$ {valor_final}
    """
    if precisa_aprovacao:
        resultado += f"\n⚠️ **ATENÇÃO:** Valor acima de R$ {teto} - Precisa aprovação do Financeiro!"
    else:
        resultado += f"\n✅ Reembolso aprovado automaticamente (abaixo de R$ {teto})."
    return resultado


# ========================================
# (Opcional) Ler TXT para usos auxiliares
# ========================================
def carregar_politica():
    try:
        with open("politica_reembolso_v1.0.txt", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "Erro: Arquivo de política não encontrado."


# ========================================
# Função para carregar Knowledge Base
# ========================================
async def load_knowledge_base(kb: Knowledge):
    """
    Carrega o conteúdo na Knowledge Base de forma assíncrona.
    """
    try:
        await kb.add_content_async(
            name="politica_reembolso",
            path="politica_reembolso_v1.0.pdf",   # nome EXATO do arquivo
            reader=PDFReader(),                   # o Agno abre o PDF e cuida do chunking
            metadata={"tipo": "politica", "fonte": "local"},
        )
        print("✅ Knowledge Base carregada com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao carregar Knowledge Base: {e}")


# ========================================
# Agente com Knowledge (RAG)
# ========================================
def criar_agente():
    """
    Cria um Agent do Agno com:
      - Knowledge (RAG) em cima de arquivo PDF:
        politica_reembolso_v1.0.pdf
      - Modelo Azure OpenAI (chat)
      - Ferramenta compute_refund
    """

    # 1) Knowledge (LanceDB + Azure Embedder)
    embedding_provider = AzureOpenAIEmbedder(
    azure_deployment="text-embedding-3-large",
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
    )

    kb = Knowledge(
        vector_db=LanceDb(
            table_name="reembolso_kb",
            uri="../tmp/lancedb",
            # search_type=LanceDb.SearchType.hybrid,
            embedder=embedding_provider
        ),
        max_results=2,
    )

    # 2) Carrega conteúdo na Knowledge Base
    asyncio.run(load_knowledge_base(kb))
    
    # Set up SQL storage for the agent's data
    db = SqliteDb(db_file="../tmp/agent_data.db")

    # 3) Modelo de chat (Azure) — id = deployment do Azure
    chat_model = AzureOpenAI(
        temperature=0.3, 
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"), 
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"), 
        api_key=os.getenv("AZURE_OPENAI_API_KEY"), 
        api_version=os.getenv("AZURE_OPENAI_MODEL_NAME")
    )

    # 4) Instruções
    instructions = """
    Você é um assistente de políticas de reembolso.
    Regras:
    - Responda SOMENTE com base nos trechos recuperados da base de conhecimento kb (RAG).
    - Cite o trecho/assunto quando possível.
    - Se precisar calcular, use a ferramenta compute_refund.
    - Se a resposta não estiver na política, diga que não encontrou.
    - Seja claro, educado e use emojis quando fizer sentido.
    """

    # 5) Cria o Agent com RAG habilitado
    agente = Agent(
        model=chat_model,
        name="Assistente de Reembolso",
        instructions=instructions,
        db=db,
        # >>> RAG
        knowledge=kb,
        search_knowledge=True,            # adiciona a ferramenta de busca na KB
        add_knowledge_to_context=True,    # injeta os trechos recuperados no contexto

        # Ferramentas
        tools=[compute_refund],

        markdown=True,
        # show_tool_calls=True,             # útil para depurar
    )
    return agente


def processar_pergunta(agente, pergunta: str):
    """
    Processa uma pergunta usando o agente.
    """
    try:
        resposta = agente.run(pergunta)
        return getattr(resposta, "content", str(resposta))
    except Exception as e:
        return f"❌ Erro ao processar pergunta: {e}"


if __name__ == "__main__":
    try:
        print("🚀 Iniciando agente de reembolso...")
        agente = criar_agente()

        while True:
            pergunta = input("💬 Digite uma pergunta: ")
            resposta = processar_pergunta(agente, pergunta)
            print(f"💬 Resposta: {resposta}")

            if pergunta == "exit" or pergunta == "sair":
                print("👋 Saindo...")
                break

            if pergunta == "teste" or pergunta == "test":
                print("💬 Testando...")

                pergunta1 = "Quais despesas são reembolsáveis e qual o prazo para solicitação?"
                print(f"\n❓ Pergunta 1: {pergunta1}")
                resposta1 = processar_pergunta(agente, pergunta1)
                print(f"💬 Resposta: {resposta1}")

                pergunta2 = "Calcule o reembolso de R$ 1.250,00"
                print(f"\n❓ Pergunta 2: {pergunta2}")
                resposta2 = processar_pergunta(agente, pergunta2)
                print(f"💬 Resposta: {resposta2}")
                
                break

    except Exception as e:
        print(f"❌ Erro ao executar o agente: {e}")
