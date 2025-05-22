from pydantic import BaseModel, Field
from datetime import date


class AddReleaseRequest(BaseModel):
    name: str = Field(title="Name",
                      description="The name of the artist",
                      max_length=100)
    type: str | None = Field(None, title="Type", description="What kind of release it is", max_length=10)
    release_date: date | None = Field(None, title="Release Date", description="The day the release came out")
    language: str | None = Field(None, title="Language",
                                 description="The language the release is in")
    country: str = Field(title="Country",
                         description="The country the artist is from",
                         max_length=50)
    artist_id: int = Field(title="Artist",
                           description="The id of the artist that made the release")
