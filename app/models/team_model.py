from pydantic import BaseModel, Field, validator
import base64

class Team(BaseModel):
    code: str = Field(..., min_length=3, max_length=3)
    name: str = Field(..., min_length=5, max_length=50)

class TeamView(Team):
    id: int
    thumbnail: str | None = Field(default=None)
    @validator("thumbnail")
    def validate_thumbnail(cls, v):
        try:
            base64.b64decode(v)
        except base64.binascii.Error:
            raise ValueError("Invalid Base64 string")
        return v
