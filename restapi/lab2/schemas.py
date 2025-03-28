from pydantic import BaseModel, Field

class BookSchema(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    author: str = Field(..., min_length=1, max_length=50)
    year: int = Field(..., ge=1000, le=2100)
