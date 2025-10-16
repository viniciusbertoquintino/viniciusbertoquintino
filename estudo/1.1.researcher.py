from agno.agent import Agent
#from agno.tools.tavily import TavilyTools
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.models.groq import Groq

from dotenv import load_dotenv
import os

load_dotenv()

model = Groq(id="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))

agent = Agent(
    model=model,
    tools=[DuckDuckGoTools()],
    debug_mode=False,
    markdown=True)

agent.print_response("use suas ferramentas para pesquisar a temperatura atual em Santo André?", stream=True)