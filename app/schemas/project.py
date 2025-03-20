from pydantic import BaseModel, Field
from datetime import datetime


class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)


class ProjectOut(BaseModel):
    id: int
    name: str
    api_token: str
    created_at: datetime
    user_id: int

    class Config:
        from_attributes = True
