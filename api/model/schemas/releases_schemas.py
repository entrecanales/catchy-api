from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import date


class CompleteRelease(BaseModel):
    id: int
    name: str
    type: Optional[str]
    release_date: Optional[date]
    language: Optional[str]
    artist_name: str

    model_config = ConfigDict(from_attributes=True)
