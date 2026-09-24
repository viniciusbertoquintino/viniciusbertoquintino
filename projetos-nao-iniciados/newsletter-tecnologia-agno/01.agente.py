from agno.agent import Agent
from agno.tools.tavily import TavilyTools
from agno.models.openai import OpenAIChat
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

data_atual = datetime.datetime.now().strftime('%d.%m.%yyyy')

agente = Agent(
    model=OpenAIChat(id="gpt-4.1-mini"),
    tools=[TavilyTools()],
    debug_mode=True
)

agente.print_response("Use suas ferramentas para pesquisar noticias de tecnologia recentes e envie um email com o resumo das noticias para meus destinatarios. Lembre-se de incluir a data atual no email: ")