from ..database import Base
from sqlalchemy import Column, UUID, String, DateTime
import uuid
from datetime import datetime, timezone

class User(Base):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True, default=uuid.uuid4,)
    user_name = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable= False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    