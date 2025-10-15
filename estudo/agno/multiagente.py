import os                              
from dotenv import load_dotenv        
from agno.agent import Agent           
from agno.models.azure.openai_chat import AzureOpenAI
from agno.team.team import Team
from agno.db.sqlite import SqliteDb
from agno.db.postgres import PostgresDb
from agno.os import AgentOS
from textwrap import dedent


load_dotenv()

# Configuração do modelo de chat
chat_model = AzureOpenAI(
    id=os.getenv("OPENAI_MODEL_NAME"),
    api_version=os.getenv("OPENAI_API_VERSION")
)


# Criação dos agentes especializados
redator = Agent(
    name="Redator",
    model=chat_model,
    role="Especialista em redação de comunicados claros para clientes",
    instructions=dedent("""
        Você é um redator de comunicados para atendimento ao cliente (CX).
        
        Sua missão:
        - Escrever um comunicado CLARO sobre política de reembolsos
        - Usar linguagem SIMPLES e DIRETA
        - Incluir: prazos, condições e como solicitar
        - Máximo de 200 palavras
        
        Objetivo: Reduzir contatos do suporte N1 (perguntas repetitivas).
    """),
    markdown=True,
)

critico = Agent(
    name="Crítico",
    model=chat_model,
    role="Analista de qualidade que identifica inconsistências e problemas",
    instructions=dedent("""
        Você é um crítico rigoroso de comunicados.
        
        Sua missão:
        - Verificar CLAREZA: O texto é fácil de entender?
        - Verificar COMPLETUDE: Faltam informações importantes?
        - Verificar AMBIGUIDADES: Algo pode ser mal interpretado?
        
        IMPORTANTE:
        - SEMPRE cite a FONTE dos problemas (qual frase/parágrafo)
        - Use o formato: "❌ Problema: [descrição] | 📍 Fonte: [trecho exato]"
        - Se estiver tudo OK, diga: "✅ Aprovado sem ressalvas"
        
        Seja específico e construtivo!
    """),
    markdown=True,
)

editor = Agent(
    name="Editor",
    model=chat_model,
    role="Editor-chefe que produz a versão final do comunicado",
    instructions=dedent("""
        Você é o editor-chefe responsável pela versão final.
        
        Sua missão:
        - Ler o texto do REDATOR
        - Ler as críticas do CRÍTICO
        - Produzir versão FINAL corrigindo todos os problemas apontados
        
        A versão final deve:
        - Ser factual e consistente
        - Ter linguagem clara e profissional
        - Não ter ambiguidades
        - Incluir cabeçalho: "📢 COMUNICADO OFICIAL - POLÍTICA DE REEMBOLSOS"
        
        Formato de saída:
        1. Versão final do comunicado
        2. Resumo das alterações feitas
    """),
    markdown=True,
)

# Criação da equipe multi-agentes
def criar_equipe_multiagentes():
    """
    Cria uma equipe de agentes especializados para produção de comunicados
    """
    team = Team(
        members=[redator, critico, editor],
        model=chat_model,
        instructions=dedent("""
            Você coordena uma equipe de 3 agentes especializados:
            
            1. REDATOR: Escreve comunicados claros sobre políticas
            2. CRÍTICO: Analisa e identifica problemas nos textos
            3. EDITOR: Produz a versão final corrigida
            
            Fluxo de trabalho:
            - Redator cria o comunicado inicial
            - Crítico analisa e aponta problemas
            - Editor produz a versão final corrigida
            
            Sempre coordene os agentes para produzir comunicados de alta qualidade.
        """),
    )
    return team



# Configuração do AgentOS
def criar_agno_os():
    """
    Cria o AgentOS para produção com a equipe multi-agentes
    """
    # Configuração do banco de dados
    if os.getenv("DATABASE_URL"):
        db = PostgresDb(db_url=os.getenv("DATABASE_URL"))
        print("🗄️ Usando PostgreSQL para produção")
    else:
        db = SqliteDb(db_file="../tmp/multiagente.db")
        print("🗄️ Usando SQLite para desenvolvimento")
    
    # Cria a equipe de agentes
    team = criar_equipe_multiagentes()
    
    # Configura o AgentOS
    agent_os = AgentOS(
        agents=[team],  # A equipe é tratada como um agente
        db=db,
        show_tool_calls=False,
        debug_mode=False,
    )
    
    print("🚀 AgentOS configurado com sucesso!")
    return agent_os

# Função para testar a equipe diretamente (desenvolvimento)
def testar_equipe_diretamente():
    """
    Testa a equipe multi-agentes diretamente (para desenvolvimento)
    """
    print("=" * 80)
    print("🚀 TESTANDO EQUIPE MULTI-AGENTES")
    print("=" * 80)
    print()
    
    team = criar_equipe_multiagentes()
    
    solicitacao = """
    Escreva um comunicado claro sobre a política de reembolsos da empresa.
    
    Informações a incluir:
    - Prazo: 30 dias após a compra
    - Condição: produto não utilizado e na embalagem original
    - Como solicitar: através do portal de atendimento ou email suporte@empresa.com
    - Tempo de processamento: até 10 dias úteis
    
    Use a equipe para criar, revisar e finalizar o comunicado.
    """
    
    print("📝 Processando solicitação com a equipe...")
    print("-" * 80)
    
    resposta = team.run(solicitacao)
    print(resposta.content)
    
    print("=" * 80)
    print("✅ TESTE CONCLUÍDO COM SUCESSO!")
    print("=" * 80)

if __name__ == "__main__":
    import sys
    
    # Verifica se deve executar em modo web ou teste
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        testar_equipe_diretamente()
    else:
        # Executa usando AgentOS para produção
        try:
            print("🌐 Iniciando AgentOS para aplicação web...")
            agent_os = criar_agno_os()
            
            # Obtém a aplicação FastAPI
            app = agent_os.get_app()
            
            print("🚀 Servidor web iniciado!")
            print("📡 Acesse: http://localhost:8000")
            print("📚 Documentação: http://localhost:8000/docs")
            print("💡 Para testar diretamente, use: python multiagente.py --test")
            
            # Inicia o servidor
            import uvicorn
            uvicorn.run(app, host="0.0.0.0", port=8000)
            
        except Exception as e:
            print(f"❌ Erro ao executar AgentOS: {e}")


