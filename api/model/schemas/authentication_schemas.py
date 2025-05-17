from datetime import date
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr


class RegisteredUser(BaseModel):
    username: str
    email: EmailStr
    display_name: str
    birth_date: date
    gender: str
    timezone: str
    is_admin: bool
    location: Optional[str]
    website: Optional[str]

    model_config = ConfigDict(from_attributes=True)
