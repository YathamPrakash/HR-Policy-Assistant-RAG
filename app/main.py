from pathlib import Path
from uuid import uuid4
from fastapi import FastAPI, HTTPException, UploadFile, File
from typing import Annotated
from fastapi.middleware.cors import CORSMiddleware


from app.schemas.chat_schema import ChatRequest, ChatResponse
from app.rag.rag_pipeline import generate_answer
from app.upload_flow import process_and_store_pdf


app=FastAPI(title="Knowledge Sphere")


#Allow CORS for frontend development(Angular frontend to communicate with FastAPI)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    # for to allow specific origins, uncomment the following lines and comment out allow_origins=["*"]
    # allow_origin=[
    #     "http://localhost:4200",
    #      "http://localhost:55449"
    # ]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"] 
)

@app.get("/")
def read_root():
    return {"message": "API is running"}

# files is the parameter name.
# UploadFile is the expected type(of file object).
# File(...) means read this parameter from the uploaded file data in the multipart request.
# ... means the parameter is required.



@app.post("/api/documents/upload")
async def upload_documents(
    files: Annotated[list[UploadFile], File()]
):
    uploaded_files = []

    # Development organization ID
    organization_id = "org_001"

    # Directory to store uploaded PDFs
    upload_directory = Path("data/documents")
    upload_directory.mkdir(parents=True, exist_ok=True)

    for file in files:

        if not file.filename or not file.filename.lower().endswith(".pdf"):
            raise HTTPException( status_code=400,detail="Only PDF files are allowed")

        # Create a unique filename
        safe_filename = Path(file.filename).name
        unique_filename = f"{uuid4()}_{safe_filename}"

        file_path = upload_directory / unique_filename

        # Save uploaded PDF
        content = await file.read()
        if not content:
           raise HTTPException(status_code=400,detail=f"{safe_filename} is empty.")
        file_path.write_bytes(content)

        try:
            # Execute complete ingestion pipeline
            ingestion_result = process_and_store_pdf(
                file_path=str(file_path),
                organization_id=organization_id
            )

            uploaded_files.append(ingestion_result)

        except Exception as exc:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to process {safe_filename}: {str(exc)}"
            )

    return {
        "message": "Documents uploaded and processed successfully",
        "total_files": len(uploaded_files),
        "uploaded_files": uploaded_files
    }


@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    # Step 3: Execute the RAG pipeline by taking user question and organization ID from the request
    answer = generate_answer(
        query=request.question,
        organization_id=request.organization_id,
        k=5
    )

    # Step 4: Return the generated answer
    return ChatResponse(answer=answer)

