
from pydantic import BaseModel, Field


# Request model
class ChatRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        description="User's question"
    )

    organization_id: str = Field(
        ...,
        min_length=1,
        description="Organization identifier"
    )


# Response model
class ChatResponse(BaseModel):
    answer: str
