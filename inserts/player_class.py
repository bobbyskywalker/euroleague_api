from pydantic import BaseModel, Field

class Player(BaseModel):
    code: int
    first_name: str
    last_name: str
    yob: int = Field(..., ge=1900, le = 2025)
