import uuid
from typing import Protocol

from .client import redis_client

class SessionStore(Protocol):
    async def create(self, session_id: str, user_id: uuid.UUID, expires: int) -> None: ...
    async def get_user_id(self, session_id: str) -> uuid.UUID | None: ...
    async def refresh(self, session_id: str, expires: int) -> None: ...
    async def delete(self, session_id: str) -> None: ...

class RedisSessionStore:
    async def create(self, session_id: str, user_id: uuid.UUID, expires: int) -> None:
        await redis_client.set(f"session:{session_id}", str(user_id), ex=expires)

    async def get_user_id(self, session_id: str) -> uuid.UUID | None:
        user_id = await redis_client.get(f"session:{session_id}")

        if user_id is None:
            return None

        if isinstance(user_id, bytes):
            user_id = user_id.decode()

        return uuid.UUID(user_id)


    async def refresh(self, session_id: str, expires: int) -> None:
        await redis_client.expire(f"session:{session_id}", expires)

    async def delete(self, session_id: str) -> None:
        await redis_client.delete(f"session:{session_id}")