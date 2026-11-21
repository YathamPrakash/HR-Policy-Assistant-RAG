
from app.config.settings import settings
from google import genai
client=genai.Client(api_key=settings.GEMINI_API_KEY);


try:
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    response= client.interactions.create(
        model=settings.CHAT_MODEL,
        input="Explain how AI works in a few words"
    )
    print(response.output_text)
except Exception as e:
    print(f"Error: {e}")
finally:
    print("Execution completed.")