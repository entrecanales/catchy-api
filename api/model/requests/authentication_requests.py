from pydantic import BaseModel, Field, EmailStr
from datetime import datetime

class RegisterRequest(BaseModel):
    username: str = Field(title="Username", description="User's login name. Can have NO spaces", max_length=50, pattern=r"^\S+$") #pattern = no spaces
    password: str = Field(title="Password", description="Password the user will use to login") #non-encrypted
    email: EmailStr = Field(title="Email", description="User email", max_length=100)
    display_name: str = Field(title="Display Name", description="Name that will be shown for the user", max_length=100)
    birth_date: datetime = Field(title="Birth Date", description="When the user was born")
    gender: str = Field(title="Gender", description="User's gender", max_length=16) #could (probably should) be an enum in the future
    timezone: str = Field(title="Timezone", description="Timezone of the user's current location", max_length=50,
                        pattern=r"^[A-Za-z]+\/[A-Za-z_\-]+$") #pattern = smth like Asia/Japan
    location: str | None = Field(title="Location", description="User's current location, can be real or not", max_length=100)
    website: str | None = Field(title="Website", description="User's website URL", max_length=100)