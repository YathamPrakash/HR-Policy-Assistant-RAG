from langchain_text_splitters import RecursiveCharacterTextSplitter
from  langchain_core.documents import Document 

def split_documents(documents:list[Document],
                    chunk_size:int=1000,
                    chunk_overlap:int=200)->list[Document]:

    # Create text splitter
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )

    # Split documents into smaller chunks
    chunks=splitter.split_documents(documents)
    if not chunks:
        raise ValueError("No chunks were created from the documents.")
    return chunks

    