import uuid

from pydantic import BaseModel


class CurrentUser(BaseModel):
    id: uuid.UUID
    username: str
    role: str
