from typing import Optional
from pydantic import BaseModel, ConfigDict
from api.model.schemas.ratings_schemas import CompleteRating


class CompleteReview(BaseModel):
    id: int
    content: str
    # rating: Optional[CompleteRating]

    model_config = ConfigDict(from_attributes=True)
