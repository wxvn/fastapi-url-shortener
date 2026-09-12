from fastapi import APIRouter, Depends, Response, Cookie
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..repositories.user import UserRepository
from ..services.auth import AuthService
from ..utils.password import Argon2PasswordHasher
from ..redis.session import RedisSessionStore
from ..schemas.user import UserResponse
from ..schemas.auth import RegisterRequest, LoginRequest

router = APIRouter(prefix="/auth", tags=["auth"])

def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    repository = UserRepository(db)
    password_hasher = Argon2PasswordHasher()
    session_store = RedisSessionStore()
    return AuthService(repository, password_hasher, session_store)

@router.post("/register", response_model=UserResponse)
async def register(data: RegisterRequest, response: Response, service: AuthService = Depends(get_auth_service)):
    user, session_id = await service.register(data.user_name, data.password)
    response.set_cookie("session_id", session_id, secure=True)
    return UserResponse(
        id=user.id,
        user_name=user.user_name,
        created_at=user.created_at,
    )

@router.post("/login", response_model=UserResponse)
async def login(data: LoginRequest, response: Response, service: AuthService = Depends(get_auth_service)):
    user, session_id = await service.login(data.user_name, data.password)
    response.set_cookie("session_id", session_id, secure=True)
    return UserResponse(
        id=user.id,
        user_name=user.user_name,
        created_at=user.created_at,
    )

@router.post("/logout")
async def logout(response: Response, session_id: str | None = Cookie(None), service: AuthService = Depends(get_auth_service)):
    if session_id is not None:
        await service.logout(session_id)
    response.delete_cookie("session_id")
    return {"detail": "logged out"}