import os
import sys
import asyncio
from dotenv import load_dotenv

load_dotenv()

from agno.agent import Agent
from agno.tools import tool
from agno.models.azure.openai_chat import AzureOpenAI
from agno.knowledge.embedder.azure_openai import AzureOpenAIEmbedder
from agno.knowledge.reader.pdf_reader import PDFReader
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.lancedb import LanceDb
from agno.db.sqlite.sqlite import SqliteDb

# Importa o sistema de memória
from memoria import MemoriaAgente


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
💰 Cálculo de Reembolso

    Valor original: R$ {valor}
    Imposto (15%): R$ {imposto}
    Valor final do reembolso: R$ {valor_final}
    """
    if precisa_aprovacao:
        resultado += f"\n⚠️ ATENÇÃO: Valor acima de R$ {teto} - Precisa aprovação do Financeiro!"
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
        api_version=os.getenv("AZURE_OPENAI_API_VERSION")
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


def processar_pergunta(agente, pergunta: str, memoria: MemoriaAgente = None):
    """
    Processa uma pergunta usando o agente com memória.
    
    Args:
        agente: O agente de IA
        pergunta: A pergunta do usuário
        memoria: (opcional) Objeto de memória para contexto
    
    Returns:
        A resposta do agente
    """
    try:
        # Se tiver memória, adiciona o contexto ao prompt
        if memoria:
            # Obtém o contexto das últimas conversas
            contexto = memoria.obter_contexto_curto_prazo()
            
            # Monta o prompt com contexto
            prompt_completo = f"{contexto}\n\n👤 Usuário: {pergunta}"
        else:
            # Sem memória, usa a pergunta diretamente
            prompt_completo = pergunta
        
        # Processa com o agente
        resposta = agente.run(prompt_completo)
        texto_resposta = getattr(resposta, "content", str(resposta))
        
        # Salva na memória (se disponível)
        if memoria:
            memoria.adicionar_mensagem("usuario", pergunta)
            memoria.adicionar_mensagem("assistente", texto_resposta)
        
        return texto_resposta
        
    except Exception as e:
        return f"❌ Erro ao processar pergunta: {e}"


if __name__ == "__main__":
    try:
        print("🚀 Iniciando agente de reembolso...")
        agente = criar_agente()
        
        # Cria a memória com buffer de 5 mensagens
        memoria = MemoriaAgente(limite_curto_prazo=10)
        print("\n")

        while True:
            pergunta = input("💬 Digite uma pergunta: ")
            
            # Comandos especiais
            if pergunta == "exit" or pergunta == "sair":
                print("👋 Saindo...")
                # Salva a sessão antes de sair
                memoria.salvar_sessao("ultima_sessao.json")
                break
            
            if pergunta == "stats" or pergunta == "estatisticas":
                memoria.mostrar_estatisticas()
                continue
            
            if pergunta == "limpar":
                memoria.limpar_tudo()
                continue

            if pergunta == "test" or pergunta == "teste":
                print("\n" + "=" * 60)
                print("💬 MODO TESTE - Conversação com memória")
                print("=" * 60 + "\n")

                pergunta1 = "Quais despesas são reembolsáveis e qual o prazo para solicitação?"
                print(f"❓ Pergunta 1: {pergunta1}")
                resposta1 = processar_pergunta(agente, pergunta1, memoria)
                print(f"🤖 Resposta: {resposta1}\n")

                pergunta2 = "Calcule o reembolso de R$ 1.250,00"
                print(f"❓ Pergunta 2: {pergunta2}")
                resposta2 = processar_pergunta(agente, pergunta2, memoria)
                print(f"🤖 Resposta: {resposta2}\n")
                
                pergunta3 = "E qual era o prazo mesmo?"  # Testa a memória!
                print(f"❓ Pergunta 3 (testando memória): {pergunta3}")
                resposta3 = processar_pergunta(agente, pergunta3, memoria)
                print(f"🤖 Resposta: {resposta3}\n")
                
                # Mostra estatísticas
                memoria.mostrar_estatisticas()
                
                break
            
            # Processa pergunta normal com memória
            resposta = processar_pergunta(agente, pergunta, memoria)
            print(f"\n🤖 Resposta: {resposta}\n")

    except Exception as e:
        print(f"❌ Erro ao executar o agente: {e}")
