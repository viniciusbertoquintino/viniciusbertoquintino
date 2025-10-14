from agno.models.groq import Groq
from agno.models.message import Message

from dotenv import load_dotenv

load_dotenv()

model = Groq(id="llama3.3-70b-versatile")

msg = Message(role="user",
              content=[{"type": "text", "text": "Ola, meu nome é Vinicius"}])

response = model.invoke(msg)

response.choices[0].message.content