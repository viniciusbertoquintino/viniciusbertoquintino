from agno.agent import Agent

from agno.models.groq import Groq
from agno.tools.hackernews import HackerNewsTools
from dotenv import load_dotenv
import os
load_dotenv()

model = Groq(id="llama-3.1-8b-instant", api_key=os.getenv("GROQ_API_KEY"))

agent = Agent(
    model=model,
    tools=[HackerNewsTools()],
    instructions="Escreva um relatório sobre o tópico. Produza apenas o relatório.",
    markdown=True,
    debug_mode=False,
    add_history_to_messages=True,
    num_history_messages=10,
)
agent.print_response("Startups e produtos em tendência.", stream=True)