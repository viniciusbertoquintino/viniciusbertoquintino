from agno.agent import Agent
from agno.tools.tavily import TavilyTools
from agno.models.openai import OpenAIChat


from agno.memory import MemoryManager #from agno.memory.v2.memory import Memory
from agno.db.sqlite import SqliteDb #from agno.memory.v2.db.sqlite import SqliteMemoryDb

from agno.os import AgentOS #from agno.playground import Playground, serve_playground_app

# Configuração da memória
memory = MemoryManager(
    model=OpenAIChat(id="gpt-4o-mini"),
    db=SqliteDb(table_name="user_memories", db_file="tmp/agent.db"),
)

# Criação do agente com memória
agent = Agent(
    model=OpenAIChat(id="gpt-4o-mini"),
    tools=[TavilyTools()],
    instructions="Você é um pesquisador especializado. Responda sempre chamando o usuário de senhor", #e use a memória para manter contexto das conversas anteriores.
    memory=memory,
    enable_agentic_memory=True,
    debug_mode=False  # Desabilitado para produção
)

agent_os = AgentOS(
    id="my-first-os",
    description="My first AgentOS",
    agents=[agent],
)

app = agent_os.get_app()

if __name__ == "__main__":
    # Default port is 7777; change with port=...
    agent_os.serve(app="my_os:app", reload=True)
