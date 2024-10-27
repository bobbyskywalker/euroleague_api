from pydantic import BaseModel, Field
from datetime import datetime

class Team(BaseModel):
    code: str = Field(..., min_length=3, max_length=3)
    name: str = Field(..., min_length=5, max_length=50)