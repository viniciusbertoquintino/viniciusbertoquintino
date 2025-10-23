from agno.agent import Agent
from agno.tools.tavily import TavilyTools
from agno.tools.yfinance import YFinanceTools
from agno.models.groq import Groq

agent = Agent(
    model=Groq(id="llama-3.3-70b-versatile"),
    tools=[YFinanceTools()],
    instructions="Use tabelas para mostrar a informação final. Não inclua nenhum outro texto.",
)

agent.print_response("Qual é cotação atual da APPLE?", stream=True)