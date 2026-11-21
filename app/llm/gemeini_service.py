from langchain_google_genai import ChatGoogleGenerativeAI
from app.config.settings import settings


llm=ChatGoogleGenerativeAI(
    model=settings.CHAT_MODEL,
    google_api_key=settings.GEMINI_API_KEY,
    temperature=0,
)

response = llm.invoke("what is Gen AI application")
print(response.text)


