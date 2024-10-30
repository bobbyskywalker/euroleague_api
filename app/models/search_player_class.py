from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime

class SearchPlayer(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    yob_from: Optional[int] = Field(ge=1950, le=datetime.now().year)
    yob_to: Optional[int] = Field(ge=1950, le=datetime.now().year)