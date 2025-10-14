from agno.agent import Agent
#from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.tavily import TavilyTools
from agno.models.groq import Groq

from dotenv import load_dotenv
import os

load_dotenv()

model = Groq(id="llama-3.1-8b-instant", api_key=os.getenv("GROQ_API_KEY"))

agent = Agent(
    model=model,
    tools=[TavilyTools()],
    debug_mode=False,
    markdown=True)

agent.print_response("use suas ferramentas para pesquisar a temperatura atual em Santo André?", stream=True)