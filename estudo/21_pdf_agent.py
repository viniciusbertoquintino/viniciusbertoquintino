from agno.agent import Agent
from agno.models.groq import Groq
from agno.knowledge.reader.pdf_reader import PDFReader
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.chroma import ChromaDB
from agno.db.sqlite import SqliteDb

# Configuração do banco vetorial
vector_db = ChromaDB(
    db_file="tmp/chroma.db",
    collection_name="pdf_agent",
)

# Configuração do conhecimento
knowledge = Knowledge(
    name="PDF Knowledge",
    path="teste.pdf",
    vector_db=vector_db,
    reader=PDFReader(chunk=True),
)

# Criação do agente
agent = Agent(
    model=Groq(id="llama3-8b-8192"),
    knowledge=knowledge,
    search_knowledge=True,
    instructions="You are a helpful assistant that can answer questions about PDF documents. Use the knowledge base to provide accurate information and cite sources when possible.",
    markdown=True,
    db=SqliteDb(db_file="tmp/agents.db"),
    add_history_to_context=True,
    num_history_runs=3,
)

# Exemplo de uso
if __name__ == "__main__":
    # Carrega o conhecimento do PDF
    knowledge.load()
    
    # Faz uma pergunta sobre o documento
    agent.print_response("What is this document about?", stream=True)