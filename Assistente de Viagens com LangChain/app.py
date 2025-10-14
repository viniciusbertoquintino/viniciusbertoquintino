# Importações necessárias
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Instruções para o assistente de viagens
instrucoes = """Você é um assistente de viagens amigável e útil. 
Sua função é ajudar as pessoas a planejar viagens, dando sugestões de:
- Destinos interessantes
- Roteiros de viagem
- Dicas práticas
- Onde comer e se hospedar

Seja sempre prestativo e dê conselhos úteis!"""

# Configura o modelo de IA (ChatGPT)
# temperature=0.7 significa que as respostas serão criativas mas não muito aleatórias
modelo_ia = ChatOpenAI(temperature=0.3, model="gpt-4o-mini")

def iniciar_assistente_viagem():
    """
    Função principal que inicia o chat com o assistente de viagens.
    """
    print("🌟 Bem-vindo ao Assistente de Viagens! 🌟")
    print("Digite 'sair' para encerrar a conversa.\n")
    
    # Loop principal do chat
    while True:
        # Pede a pergunta do usuário
        pergunta_usuario = input("Você: ")
        
        # Verifica se o usuário quer sair
        if pergunta_usuario.lower() in ["sair", "exit", "tchau"]:
            print("✈️ Assistente: Até mais! Aproveite sua viagem! ✈️")
            break
        
        # Cria a mensagem completa para a IA
        mensagem_completa = f"{instrucoes}\n\nPergunta do usuário: {pergunta_usuario}"
        
        try:
            # Envia a pergunta para a IA e recebe a resposta
            resposta = modelo_ia.invoke(mensagem_completa)
            print(f"🗺️ Assistente: {resposta.content}\n")
            
        except Exception as erro:
            print(f"❌ Erro: {erro}")
            print("Verifique se sua chave da OpenAI está configurada corretamente.\n")

# Executa o programa quando este arquivo é executado diretamente
if __name__ == "__main__":
    iniciar_assistente_viagem()