from pydantic import BaseModel, Field, EmailStr, field_validator
from datetime import datetime


class RegisterRequest(BaseModel):
    username: str = Field(title="Username", description="User's login name. Can have NO spaces",
                          max_length=50, pattern=r"^\S+$")  # pattern = no spaces
    password: str = Field(title="Password", description="Password the user will use to login",  # non-encrypted
                          min_length=8)
    # minimum 1 number, 1 uppercase, 1 lowercase and 1 symbol
    email: EmailStr = Field(title="Email", description="User email", max_length=100)
    display_name: str = Field(title="Display Name", description="Name that will be shown for the user", max_length=100)
    birth_date: datetime = Field(title="Birth Date", description="When the user was born")
    gender: str = Field(title="Gender", description="User's gender", max_length=16)
    # could (probably should) be an enum in the future
    timezone: str = Field(title="Timezone", description="Timezone of the user's current location", max_length=50,
                          pattern=r"^[A-Za-z]+\/[A-Za-z_\-]+$")  # pattern = smth like Asia/Japan
    # America/New York and similar should have a _ instead of a space
    location: str | None = Field(None, title="Location", description="User's current location, can be real or not",
                                 max_length=100)
    website: str | None = Field(None, title="Website", description="User's website URL", max_length=100)

    @field_validator('password')
    def check_password(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError("Password should at least have an upper case letter")
        if not any(c.islower() for c in v):
            raise ValueError("Password should at least have an lower case letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password should at least have a number")
        if not any(c in '@$!%*?&' for c in v):
            raise ValueError("Password should have at least a punctuation sign")
        return v


class LoginRequest(BaseModel):
    username: str = Field(title="Username", description="User's login name. Can have NO spaces",
                          max_length=50, pattern=r"^\S+$")  # pattern = no spaces
    password: str = Field(title="Password", description="Password the user will use to login")  # non-encrypted
