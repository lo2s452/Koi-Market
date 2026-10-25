import uuid

from pydantic import BaseModel, ConfigDict, Field

from app.models import Role


class Credentials(BaseModel):
    model_config = ConfigDict(extra="forbid")

    username: str = Field(min_length=3, max_length=32, pattern=r"^[A-Za-z0-9_]+$")
    password: str = Field(min_length=8, max_length=128)


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    username: str
    role: Role


class AccessToken(BaseModel):
    access_token: str
    token_type: str = "Bearer"
    expires_in: int
