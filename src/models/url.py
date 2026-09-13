from ..database import Base

from sqlalchemy import Column, UUID, String, DateTime, ForeignKey, Integer

import uuid

from datetime import datetime, timezone


class URL(Base):
    __tablename__ = "urls"

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID, ForeignKey("users.id"), nullable=False)

    original_url = Column(String, nullable=False)
    short_code = Column(String, unique=True, nullable=False)

    clicks = Column(Integer, nullable=False, default=0)

    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

