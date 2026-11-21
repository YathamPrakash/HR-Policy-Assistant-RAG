from app.retrieval.retriever import retrieve_relevant_document
from app.llm.gemeini_service import llm


from langchain_core.prompts import PromptTemplate,ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import StrOutputParser


prompt=ChatPromptTemplate.from_template("""
You are KnowSphere AI, an enterprise document assistant.

Answer the question using only the provided context.

If the answer is not available in the context,
say that you could not find the information
in the uploaded documents.

Context:
{context}

Question:
{question}

Answer:
""")


def format_docs(documents):
    return "\n\n".join(document.page_content for document in documents)


rag_chain=(
    {
        "context":RunnableLambda(
            lambda inputs:format_docs(
                retrieve_relevant_document(
                    query=inputs['question'],
                    organization_id=inputs['organization_id'],
                    k=inputs.get("k", 5)
                ))

        ),
        "question":RunnableLambda(
            lambda inputs: inputs['question']
        )
    }
    |prompt
    |llm
    |StrOutputParser(strip=True)
)



# 4.  function to invoke RAG chain
def generate_answer(
    query: str,
    organization_id: str,
    k: int = 5) -> str:

    if not query or not query.strip():
        raise ValueError("Please provide a valid question.")

    if not organization_id or not organization_id.strip():
        raise ValueError("Please provide organization_id.")

    return rag_chain.invoke({
        "question": query,
        "organization_id": organization_id,
        "k": k
    })
