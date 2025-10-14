from agno.agent import Agent
from agno.models.groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

model = Groq(id="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))

agent = Agent(
    model=model,
    debug_mode=False,
    markdown=True
)

agent.print_response("Ola, meu nome é Vinicius", stream=True)