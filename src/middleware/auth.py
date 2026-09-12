from uuid import UUID

from fastapi import Cookie, Response

from ..errors import UnauthorizedError
from ..redis.session import RedisSessionStore

SESSION_TTL = 60 * 60 * 24 * 7

session_store = RedisSessionStore()

async def auth(response: Response, session_id: str | None = Cookie(None)) -> UUID:
    if session_id is None:
        raise UnauthorizedError()

    user_id = await session_store.get_user_id(session_id)

    if user_id is None:
        raise UnauthorizedError()

    await session_store.refresh(session_id, SESSION_TTL)

    response.set_cookie(
        "session_id",
        session_id,
        max_age=SESSION_TTL,
        httponly=True,
        secure=True,
    )

    return user_id