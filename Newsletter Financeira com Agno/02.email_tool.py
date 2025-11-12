from email.message import EmailMessage
from dotenv import load_dotenv
import os, smtplib

load_dotenv()
EMAIL_ADDRESS= os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
DESTINATARIOS = os.getenv("DESTINATARIOS", "")

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
    
if __name__ == '__main__':
    assunto_test = "Email de teste"
    conteudo_test= "Essa é uma mensagem de teste!"

    resposta= envia_email_tool(assunto_test, conteudo_test)
    print(resposta)
    


