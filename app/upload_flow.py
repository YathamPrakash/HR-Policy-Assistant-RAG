from app.ingestion.pdf_loader import load_pdf
from pathlib import Path
from app.ingestion.text_cleaner import clean_documents
from app.ingestion.text_splitter import split_documents

from app.vectorstore.vectorstore_service import chunks_store_to_vector_db


def process_and_store_pdf(file_path: str, organization_id: str):
    # Load PDF
    documents = load_pdf(file_path)
    print(f"Loaded {len(documents)} pages from {file_path}")

    # Clean documents
    cleaned_documents = clean_documents(documents)
    print(f"Cleaned {len(cleaned_documents)} pages from {file_path}")

    # Split documents into chunks
    chunks = split_documents(cleaned_documents)
    print(f"Split into {len(chunks)} chunks from {file_path}")

    # Store chunks to vector database
    # Step 4: Store chunks in Pinecone
    storage_result = chunks_store_to_vector_db(
        chunks=chunks,
        organization_id=organization_id
    )
    print(f"Stored chunks for {file_path} in vector database")
    return {
        "message": "Document ingested successfully",
        "filename": Path(file_path).name,
        "total_pages": len(documents),
        "total_cleaned_pages": len(cleaned_documents),
        "total_chunks": len(chunks),
        "storage": storage_result
    }

