from pydantic import BaseModel, Field


class AddReviewRequest(BaseModel):
    user: str = Field(title="User Name",
                      description="The name of the user writing the review")
    score: int = Field(title="Score",
                       description="The score of the review",
                       ge=0,
                       le=100)
    release_id: int = Field(title="Release Id",
                            description="The id of the release (the album, single...)")
    content: str = Field(title="Content",
                         description="The content of the review",
                         max_length=1000)


class UpdateReviewRequest(BaseModel):
    score: int = Field(title="Score",
                       description="The score of the review",
                       ge=0,
                       le=100)
    content: str = Field(title="Content",
                         description="The content of the review",
                         max_length=1000)
