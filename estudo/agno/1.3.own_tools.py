from agno.agent import Agent
#from agno.tools.tavily import TavilyTools
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.models.groq import Groq

from dotenv import load_dotenv
import os

load_dotenv()

model = Groq(id="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))


def celsius_to_fahrenheit(temperature_celsius: float) -> float:
    """
    Converte a temperatura de Celsius para Fahrenheit.

    Args:
        temperature_celsius (float): A temperatura em Celsius.
    Returns:
        float: A temperatura em Fahrenheit.
    """
    return (temperature_celsius * 9/5) + 32

agent = Agent(
    model=model,
    #tools=[TavilyTools()],
    tools=[DuckDuckGoTools(), celsius_to_fahrenheit()],
    debug_mode=False,
    markdown=True)

agent.print_response("Use suas ferramentas para pesquisar a temperatura de hoje em Santo André em graus Celsius?", stream=True)