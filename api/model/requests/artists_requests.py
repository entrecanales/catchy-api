from pydantic import BaseModel, Field
from datetime import datetime


class AddArtistRequest(BaseModel):
    name: str = Field(title="Name",
                      description="The name of the artist",
                      max_length=50)
    also_known_as: str | None = Field(None, title="Also Known As",
                                      description="Alternate names of the artist, separated by commas")
    active_since: int | None = Field(None, title="Active Since",
                                     description="The year the artist has been active since",
                                     ge=0,
                                     le=datetime.now().year)
    inactive_since: int | None = Field(None, title="Inactive Since",
                                       description="The year the artist has been inactive since",
                                       ge=0,
                                       le=datetime.now().year)
    country: str = Field(title="Country",
                         description="The country the artist is from",
                         max_length=50)
    official_website: str | None = Field(None, title="Official Website",
                                         description="The artist's official website")
    spotify_url: str | None = Field(None, title="Spotify URL",
                                    description="The URL for the artist's Spotify page")
    is_group: bool = Field(False, title="Is Group",
                           description="If the artist is a group")
