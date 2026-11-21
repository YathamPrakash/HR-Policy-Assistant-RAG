from dotenv import load_dotenv
from google import genai
from app.config.settings import settings

load_dotenv()
client = genai.Client(api_key=settings.GEMINI_API_KEY)

try:
    models = client.models.list()
    print("\nModels available to your API key:\n")
    for model in models:
        print(f"modelname :{model.name}")
        print(f"Display Name: {model.display_name}")
        print(f"Description: {model.description}")
        print('\n\n')


except Exception as error:
    print("Unable to retrieve models.")
    print(type(error).__name__, str(error))