from langchain.chat_models import init_chat_model
import os
from dotenv import load_dotenv
load_dotenv()

from rich import print

llm = init_chat_model("groq:llama-3.1-8b-instant")
#llm = init_chat_model("google_genai:gemini-2.5-flash")

system_message = SystemMessage(

    content
)

response = llm.invoke("Olá, como vai?")
print(response)