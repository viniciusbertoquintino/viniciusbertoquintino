from agno.agent import Agent
from agno.tools.tavily import TavilyTools
from agno.models.openai import OpenAIChat
from dotenv import load_dotenv
from email.message import EmailMessage
import os, smtplib, time
from datetime import datetime

load_dotenv()
EMAIL_ADDRESS= os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
DESTINATARIOS = os.getenv("DESTINATARIOS", "")
HORA_ENVIO = os.getenv("SEND_AT", "")#HH:MM - SEND_AT= 11:20

def envia_email_tool(assunto, conteudo):
    """Envio de emails"""
    try:
        msg= EmailMessage()
        msg['Subject']= assunto
        msg['From']= EMAIL_ADDRESS
        msg['To'] = DESTINATARIOS

        msg.set_content(conteudo, charset='utf-8')

        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        
        return "Email enviado com sucesso!!!"

    except Exception as e:
        return f'Erro: {e}'

agente = Agent(
    model=OpenAIChat(id="gpt-4.1-mini"),
    tools=[TavilyTools(), envia_email_tool],
    debug_mode=False
)

    
if __name__ == '__main__':
    from prompt import prompt_pro_agente

    #agente.run(prompt_pro_agente)

    print(f"Agendamento de envio da newsletter às {HORA_ENVIO}")
    ultimo_envio = None

    while True:
        agora = datetime.now()

        if agora.strftime("%H:%M") == HORA_ENVIO and ultimo_envio != agora.date:
            print("Executando a newsletter...")

            try:
                prompt_data = f"DATA: {agora:%d/%m/%y}\n\n {prompt_pro_agente}"
                agente.run(prompt_data)
                ultimo_envio = agora.date()
                print("Newsletter enviada!!!")
                time.sleep(65)
            
            except Exception as e:
                print(f"Erro: {e}")
                time.sleep(10)
        else:
            time.sleep(10)        
