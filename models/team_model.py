from pydantic import BaseModel, Field


class Team(BaseModel):
    code: str = Field(..., min_length=3, max_length=3)
    name: str = Field(..., min_length=5, max_length=50)
