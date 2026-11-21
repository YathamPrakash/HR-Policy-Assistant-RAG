from langchain_core.documents import Document

from app.embeddings.embedding_service import embedding_model
from app.vectorstore.vectorstore_service import create_pinecone_index, initialize_pinecone_index


def retrieve_relevant_document( query: str,
    organization_id: str,
    k: int = 5)->list[Document]:

    #validate input
    if not query or query.strip() == "":
        raise ValueError("Please provide inputquery")
    
    if not organization_id or organization_id.strip() == "":
        raise ValueError("Please provide organization_id")
    
    if k <= 0:
        raise ValueError("k must be greater than zero.")
    
    vector_store = initialize_pinecone_index(organization_id=organization_id)
    
    relevant_documents=vector_store.similarity_search(
        query=query,
        k=k
    )
      # 5. Return retrieved documents
    return relevant_documents

 


    