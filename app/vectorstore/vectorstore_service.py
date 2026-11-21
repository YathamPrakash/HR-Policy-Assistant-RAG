
from pinecone import Pinecone, ServerlessSpec
from langchain_core.documents import Document
from langchain_pinecone import PineconeVectorStore

from app.config.settings import settings
from app.embeddings.embedding_service import (
    embedding_model,
    embedding_dimensions
)

pinecone = Pinecone(api_key=settings.PINECONE_API_KEY)


def create_pinecone_index():
    index_name = settings.PINECONE_INDEX_NAME

    # 1. Check whether index exists
    if not pinecone.has_index(index_name):
        pinecone.create_index(
            name=index_name,
            dimension=embedding_dimensions,
            metric="cosine",
            spec=ServerlessSpec(
                cloud=settings.PINECONE_CLOUD,
                region=settings.PINECONE_REGION
            )
        )
        print(f"Index '{index_name}' created successfully.")
    else:
        print(f"Index '{index_name}' already exists.")

    # 2. Validate index dimension
    index_info = pinecone.describe_index(index_name)

    if index_info.dimension != embedding_dimensions:
        raise ValueError("Pinecone index dimension mismatch.")

    # 3. Return connected index
    return pinecone.Index(index_name)

def initialize_pinecone_index(organization_id: str):
    """Initialize Pinecone index if it doesn't exist."""
        # 1. Connect to Pinecone
    index = create_pinecone_index()

    # 2. Initialize LangChain vector store
    vector_store = PineconeVectorStore(
        index=index,
        embedding=embedding_model,
        namespace=organization_id
    )
    return vector_store

def chunks_store_to_vector_db(
    chunks: list[Document],
    organization_id: str
):
    """Store document chunks in Pinecone using LangChain."""

    if not chunks:
        raise ValueError("No chunks provided for storage.")

    # 2. Initialize LangChain vector store
    vector_store = initialize_pinecone_index(organization_id=organization_id)

    # 3. Generate embeddings internally and store documents
    ids = vector_store.add_documents(documents=chunks)

    return {
        "message": f"Stored {len(ids)} chunks successfully.",
        "total_chunks": len(ids),
        "ids": ids,
        "namespace": organization_id
    }
