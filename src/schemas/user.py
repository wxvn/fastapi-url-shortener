from datetime import datetime
import uuid

from pydantic import BaseModel, Field

class UserUpdate(BaseModel):
    user_name: str | None = Field(None, min_length=2, max_length=64)
    old_password: str | None = Field(None, min_length=6, max_length=128)
    new_password: str | None = Field(None, min_length=6, max_length=128)

class UserResponse(BaseModel):
    id: uuid.UUID
    user_name: str
    created_at: datetime