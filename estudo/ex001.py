from langchain.chat_models import init_chat_model
import os
from dotenv import load_dotenv
load_dotenv()

llm = init_chat_model("groq:llama-3.1-8b-instant")

response = llm.invoke("Olá, como vai?")
print(response)