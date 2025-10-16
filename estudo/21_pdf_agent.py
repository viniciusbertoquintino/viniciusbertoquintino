from agno.agent import Agent
from agno.models.groq import Groq
from agno.db.sqlite import SqliteStorage
from dotenv import load_dotenv
import os
load_dotenv()

from agno.knowledge.pdf import PDFReader, PDFKnowledge
from agno.vectordb.chroma import ChromaDB

vector_db = ChromaDB(
    db_file="tmp/chroma.db",
    collection_name="pdf_agent",
)

knowledge = Knowledge(
    name="PDF Knowledge",
    path="teste.pdf",
    vector_db=vector_db,
    reader=PDFReader(chunk=True),
)

agent = Agent(