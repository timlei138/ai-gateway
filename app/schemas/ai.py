from pydantic import BaseModel, Field


class OpenAIRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=2000)
    max_tokens: int = Field(100, ge=10, le=1000)
    stream: bool = False
