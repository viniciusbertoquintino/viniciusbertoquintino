"""
=== SISTEMA MULTI-AGENTES: REDATOR → CRÍTICO → EDITOR ===

Este código cria 3 agentes que trabalham juntos para produzir
um comunicado claro sobre reembolsos.

FLUXO:
1. REDATOR: Escreve o comunicado inicial
2. CRÍTICO: Analisa e aponta problemas (com fontes)
3. EDITOR: Revisa e produz versão final

Máximo de 2 rodadas para evitar loops infinitos.
"""

# ============================================================================
# PARTE 1: IMPORTAR BIBLIOTECAS E CARREGAR VARIÁVEIS DE AMBIENTE
# ============================================================================
# Importamos as ferramentas do Agno que vamos usar

import os                              # Para acessar variáveis de ambiente
from dotenv import load_dotenv         # Para carregar o arquivo .env
from agno.agent import Agent           # Classe para criar agentes individuais
from agno.models.azure.openai_chat import AzureOpenAI  # Modelo Azure OpenAI
from textwrap import dedent            # Remove indentação de textos

# Carrega as variáveis do arquivo .env para o ambiente
load_dotenv()

# Verifica se as variáveis necessárias estão configuradas
chat_model = AzureOpenAI(
        id=os.getenv("OPENAI_MODEL_NAME"),
        api_version=os.getenv("OPENAI_API_VERSION")
    ),
# ============================================================================
# PARTE 2: CRIAR O AGENTE REDATOR
# ============================================================================
# O Redator é responsável por escrever o comunicado inicial

redator = Agent(
    # Nome do agente (para identificação)
    name="Redator",
    
    # Modelo de IA usando Azure OpenAI (configurado no .env)
    
    model= chat_model,
    
    # Papel do agente na equipe
    role="Especialista em redação de comunicados claros para clientes",
    
    # Instruções detalhadas sobre como o agente deve agir
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


# ============================================================================
# PARTE 3: CRIAR O AGENTE CRÍTICO
# ============================================================================
# O Crítico analisa o texto do Redator e aponta problemas

critico = Agent(
    name="Crítico",

   model= chat_model,

    role="Analista de qualidade que identifica inconsistências e problemas",
    
    instructions=dedent("""
        Você é um crítico rigoroso de comunicados.
        
        Sua missão:
        - Verificar CLAREZA: O texto é fácil de entender?
        - Verificar COMPLETUDE: Faltam informações importantes?
        - Verificar AMBIGUIDADES: Algo pode ser mal interpretado?
        
        IMPORTANTE:
        - SEMPRE cite a FONTE dos problemas (qual frase/parágrafo)
        - Use formato: "❌ Problema: [descrição] | 📍 Fonte: [trecho exato]"
        - Se estiver tudo OK, diga: "✅ Aprovado sem ressalvas"
        
        Seja específico e construtivo!
    """),
    
    
    markdown=True,
)


# ============================================================================
# PARTE 4: CRIAR O AGENTE EDITOR
# ============================================================================
# O Editor produz a versão final baseado no feedback do Crítico

editor = Agent(

    name="Editor",

    model= chat_model,

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


# ============================================================================
# PARTE 5: FUNÇÃO PRINCIPAL - ORQUESTRAÇÃO DOS AGENTES
# ============================================================================
# Esta função coordena os 3 agentes em sequência

def executar_sistema_multiagentes():
    """
    Executa o fluxo completo do sistema multi-agentes.
    
    Fluxo:
    1. Redator escreve → 2. Crítico analisa → 3. Editor finaliza
    """
    
    print("=" * 80)
    print("🚀 INICIANDO SISTEMA MULTI-AGENTES")
    print("=" * 80)
    print()
    
    # ------------------------------------------------------------------------
    # RODADA 1: REDATOR ESCREVE O COMUNICADO INICIAL
    # ------------------------------------------------------------------------
    print("📝 ETAPA 1: Redator escrevendo comunicado inicial...")
    print("-" * 80)
    
    # Criamos a solicitação (prompt) para o Redator
    solicitacao_inicial = """
    Escreva um comunicado claro sobre a política de reembolsos da empresa.
    
    Informações a incluir:
    - Prazo: 30 dias após a compra
    - Condição: produto não utilizado e na embalagem original
    - Como solicitar: através do portal de atendimento ou email suporte@empresa.com
    - Tempo de processamento: até 10 dias úteis
    """
    
    # O Redator gera a resposta (comunicado inicial)
    resposta_redator = redator.run(solicitacao_inicial)
    texto_inicial = resposta_redator.content
    
    print(texto_inicial)
    print()
    
    # ------------------------------------------------------------------------
    # RODADA 2: CRÍTICO ANALISA O TEXTO DO REDATOR
    # ------------------------------------------------------------------------
    print("🔍 ETAPA 2: Crítico analisando o comunicado...")
    print("-" * 80)
    
    # O Crítico recebe o texto do Redator e analisa
    solicitacao_critica = f"""
    Analise este comunicado sobre reembolsos:
    
    {texto_inicial}
    
    Identifique problemas de clareza, completude ou ambiguidade.
    Cite a fonte específica de cada problema.
    """
    
    resposta_critico = critico.run(solicitacao_critica)
    analise_critica = resposta_critico.content
    
    print(analise_critica)
    print()
    
    # ------------------------------------------------------------------------
    # RODADA 3: EDITOR PRODUZ VERSÃO FINAL
    # ------------------------------------------------------------------------
    print("✍️ ETAPA 3: Editor produzindo versão final...")
    print("-" * 80)
    
    # O Editor recebe TANTO o texto inicial QUANTO as críticas
    solicitacao_final = f"""
    Produza a versão final do comunicado considerando:
    
    TEXTO ORIGINAL DO REDATOR:
    {texto_inicial}
    
    ANÁLISE DO CRÍTICO:
    {analise_critica}
    
    Corrija todos os problemas apontados e entregue a versão final.
    """
    
    resposta_editor = editor.run(solicitacao_final)
    versao_final = resposta_editor.content
    
    print(versao_final)
    print()
    
    # ------------------------------------------------------------------------
    # FIM: SISTEMA CONCLUÍDO
    # ------------------------------------------------------------------------
    print("=" * 80)
    print("✅ SISTEMA MULTI-AGENTES CONCLUÍDO COM SUCESSO!")
    print("=" * 80)


# ============================================================================
# PARTE 6: EXECUTAR O PROGRAMA
# ============================================================================
# Esta linha garante que o código só executa quando rodamos diretamente
# (não quando importamos como módulo)

if __name__ == "__main__":
    # Executa a função principal
    executar_sistema_multiagentes()


