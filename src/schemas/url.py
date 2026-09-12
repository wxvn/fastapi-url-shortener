from datetime import datetime
import uuid

from pydantic import BaseModel, Field

class URLBase(BaseModel):
    original_url: str = Field(..., min_length=1, max_length=2048)

class URLCreate(URLBase):
    pass

class URLUpdate(BaseModel):
    original_url: str | None = Field(None, min_length=1, max_length=2048)
    short_code: str | None = Field(None, min_length=1, max_length=64)

class URLResponse(URLBase):
    id: uuid.UUID
    short_code: str
    clicks: int
    created_at: datetime