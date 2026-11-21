import re
from langchain_core.documents import Document

def clean_documents(documents: list[Document]) -> list[Document]:
    cleaned_documents=[]
    for document in documents:
        text=document.page_content
        # 1. Normalize line endings
        text = text.replace("\r\n", "\n").replace("\r", "\n")
        # 2. Replace multiple spaces and tabs with a single space
        text = re.sub(r"[ \t]+", " ", text)
        # 3. Replace excessive blank lines with a single blank line
        text = re.sub(r"\n{3,}", "\n\n", text)        
        # 4. Remove leading and trailing whitespace
        text = text.strip()
        # 5. Ignore empty documents
        if not text:
            continue
        cleaned_documents.append(Document(page_content=text, metadata=document.metadata.copy()))
    if not cleaned_documents:
        raise ValueError("No valid text available after cleaning.")
    return cleaned_documents