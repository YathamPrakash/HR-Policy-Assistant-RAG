from pypdf import PdfReader
from langchain_core.documents import Document


def load_pdf(file_path:str)->list[Document]:
    reader = PdfReader(str(file_path))
    pages: list[Document] = []
    for i,page in enumerate(reader.pages,start=1):
        text=page.extract_text().strip() or ""
        if text:
            pages.append(
                Document(
                    page_content=text,
                    metadata={"page": i}
                )
            )
    if not pages:
        raise ValueError("No text found in PDF pages.")
    return pages

