from agno.agent import Agent
from agno.playground import Playground, serve_playground_app
from agno.storage.sqlite import SqliteStorage
from agno.models.openai import OpenAIChat

from agno.knowledge.pdf import PDFKnowledgeBase, PDFReader
from agno.vectordb.chroma import ChromaDb



# RAG
vector_db = ChromaDb(collection="pdf_agent", path="tmp/chromadb", persistent_client=True)

knowledge = PDFKnowledgeBase(
path="GlobalEVOutlook2025.pdf",
vector_db=vector_db,
reader=PDFReader(chunk=True)
)
# knowledge.load()


db = SqliteStorage(table_name="agent_session", db_file="tmp/agent.db")

agent = Agent(
    name="Agente de PDF",
    model=OpenAIChat(id="gpt-4.1-mini"),
    storage=db,
    knowledge=knowledge,
    instructions="Você deve chamar o usuário de senhor",
    description="",
    add_history_to_messages=True,
    search_knowledge=True, 
    num_history_runs=3,
    # debug_mode=True
)

app = Playground(agents=[
        agent
]).get_app()


if __name__ == "__main__":
    # knowledge.load(recreate=True)
    serve_playground_app("21_pdf_agent:app", reload=True)







