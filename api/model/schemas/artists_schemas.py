from typing import Optional
from pydantic import BaseModel, ConfigDict


class AddedArtist(BaseModel):
    id: int
    name: str
    also_known_as: Optional[str]
    active_since: Optional[int]
    inactive_since: Optional[int]
    country: Optional[str]
    official_website: Optional[str]
    spotify_url: Optional[str]
    is_group: Optional[bool]

    model_config = ConfigDict(from_attributes=True)
