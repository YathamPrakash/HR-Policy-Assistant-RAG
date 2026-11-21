
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.config.settings import settings


# 1. Initialize Gemini embedding model once
embedding_model = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=settings.GEMINI_API_KEY,
    output_dimensionality=settings.GEMINI_EMBEDDING_DIMENSIONS
)


# 2. Validate and get embedding dimensions
def validate_embedding_dimensions():

    test_embedding = embedding_model.embed_query("Test")

    actual_dimensions = len(test_embedding)
    expected_dimensions = settings.GEMINI_EMBEDDING_DIMENSIONS

    if actual_dimensions != expected_dimensions:
        raise ValueError(
            f"Embedding dimension mismatch. "
            f"Expected: {expected_dimensions}, "
            f"Actual: {actual_dimensions}"
        )

    return actual_dimensions


# 3. Get validated dimensions
embedding_dimensions = validate_embedding_dimensions()
