from agno.agent import Agent
#from agno.tools.duckduckgo import DuckDuckGoTools
#from agno.tools.tavily import TavilyTools
from agno.tools.yfinance import YFinanceTools
from agno.models.groq import Groq

from dotenv import load_dotenv
import os

load_dotenv()

model = Groq(id="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))

agent = Agent(
    model=model,
    tools=[YFinanceTools()],
    instructions="Use tabelas para mostrar a informação final. Não inclua nenhum outro texto.",
    #max_iterations=3,
    debug_mode=False,
    markdown=True)

agent.print_response("Qual é cotação atual da empresa Microsoft?", stream=True)