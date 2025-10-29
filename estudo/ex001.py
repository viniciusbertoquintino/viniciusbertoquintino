from langchain.chat_models import init_chat_model

llm = init_chat_model("ollama:gpt-oss:20b")

llm = init_chat_model("groq:llama-3.1-8b-instant")

response = llm.invoke("Olá, como vai?")
print(response)