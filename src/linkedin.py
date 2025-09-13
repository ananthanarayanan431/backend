
from dotenv import load_dotenv
load_dotenv()
from langchain_openai.chat_models import ChatOpenAI

llm = ChatOpenAI(model="gpt-5-nano-2025-08-07")

response = llm.invoke("Hey I'm Anantha")
print(response)