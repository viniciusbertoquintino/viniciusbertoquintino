from agno.agent import Agent
#from agno.models.openai import OpenAIChat
from agno.models.groq import Groq
from agno.os import AgentOS
import os
from dotenv import load_dotenv
load_dotenv()

assistant = Agent(
    name="Assistant",
    #model=OpenAIChat(id="gpt-5-mini"),
    model=Groq(id="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY")),
    instructions=["You are a helpful AI assistant."],
    markdown=True,
)

agent_os = AgentOS(
    id="my-first-os",
    description="My first AgentOS",
    agents=[assistant],
)

app = agent_os.get_app()

if __name__ == "__main__":
    # Default port is 7777; change with port=...
    agent_os.serve(app="my_os:app", reload=True)