from agno.agent import Agent
from agno.tools.tavily import TavilyTools
from agno.models.openai import OpenAIChat
# from agno.models.groq import Groq

from agno.storage.sqlite import SqliteStorage

from agno.playground import Playground, serve_playground_app


def celsius_to_fh(temperatura_celsius: float):
    """
    Converte temperatura de Celsius para Fahrenheit.

    Args:
        temperatura_celsius (float): Temperatura em graus Celsius

    Returns:
        float: Temperatura convertida para Fahrenheit
    """
    return (temperatura_celsius * 9/5) + 32



db = SqliteStorage(table_name="agent_session", db_file="tmp/agent.db")

agent = Agent(
    # model=Groq(id="llama-3.3-70b-versatile"),
    name="Agente do tempo",
    model=OpenAIChat(id="gpt-4.1-mini"),
    tools=[
        TavilyTools(),
        celsius_to_fh,
        ],
    storage=db,
    add_history_to_messages=True,
    num_history_runs=3,
    # debug_mode=True
)



app = Playground(agents=[
        agent
]).get_app()


if __name__ == "__main__":
    serve_playground_app("13_own_tools:app", reload=True)



# agent.print_response("Use suas ferramentas para pesquisar a temperatura de hoje em Porto Alegre em Fahrenheit")