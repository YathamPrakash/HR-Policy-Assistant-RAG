from pydantic_settings import BaseSettings ,SettingsConfigDict

class Settings(BaseSettings):

    #Required api keys for external services
    PINECONE_API_KEY: str
    GEMINI_API_KEY: str
    GROQ_API_KEY:str
    GEMINI_EMBEDDING_DIMENSIONS: int

    #  OpenAI model configuration
    CHAT_MODEL:str
    EMBEDDING_MODEL: str

    #PINECONE model configuration
    PINECONE_INDEX_NAME:str
    PINECONE_CLOUD: str = "aws"
    PINECONE_REGION: str = "us-east-1"


    model_config=SettingsConfigDict(
        env_file=".env",
        encoding="utf-8",
        extra="ignore"
    )

settings=Settings()



  

