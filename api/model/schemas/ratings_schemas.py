from pydantic import BaseModel, ConfigDict


class CompleteRating(BaseModel):
    id: int
    user_fk: int
    release_fk: int
    score: int

    model_config = ConfigDict(from_attributes=True)
