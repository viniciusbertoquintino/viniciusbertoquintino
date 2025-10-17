from agno.agent import Agent
#from agno.models.openai import OpenAIChat
from agno.models.groq import Groq
from agno.os import AgentOS

from agno.tools.duckduckgo import DuckDuckGoTools

import os
from dotenv import load_dotenv
load_dotenv()

#memoria do agente
from agno.db.sqlite import SqliteDb
memory_db = SqliteDb(db_file="tmp/agent.db")

model = Groq(id="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))

assistant = Agent(
    name="Assistente do Vinicius",
    #model=OpenAIChat(id="gpt-5-mini"),
    model=model,
    tools=[DuckDuckGoTools()],
    instructions=["Você é um assistente de IA. Responda sempre chamando o usuário de senhor."],
    markdown=True,
    db=memory_db,
    enable_user_memories=True,
    enable_agentic_memory=True,
    
)

agent_os = AgentOS(
    id="my-first-os",
    description="My first AgentOS",
    agents=[assistant],
)

app = agent_os.get_app()

if __name__ == "__main__":
    # Default port is 7777; change with port=...
    agent_os.serve(app="31_memory_simples:app", reload=True)