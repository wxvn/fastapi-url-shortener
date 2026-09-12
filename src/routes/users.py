from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..repositories.user import UserRepository
from ..schemas.pagination import Pagination
from ..schemas.user import UserResponse, UserUpdate
from ..services.user import UserService
from ..utils.password import Argon2PasswordHasher

from ..middleware import auth

router = APIRouter(prefix="/users", tags=["users"])


def get_user_service(db: AsyncSession = Depends(get_db)) -> UserService:
    repository = UserRepository(db)
    password_hasher = Argon2PasswordHasher()

    return UserService(repository, password_hasher)



@router.get("/", response_model=list[UserResponse], dependencies=[Depends(auth)])
async def get_users(pagination: Pagination = Depends(), service: UserService = Depends(get_user_service)):
    users = await service.get_users(pagination.limit, pagination.offset)
    res = []

    for user in users:
        res.append(
            UserResponse(
                id=user.id,
                user_name=user.user_name,
                created_at=user.created_at,
            )
        )

    return res

@router.get("/me", response_model=UserResponse)
async def get_me(current_user_id: UUID = Depends(auth), service: UserService = Depends(get_user_service)):
    user = await service.get_user(current_user_id)

    res = UserResponse(
        id=user.id,
        user_name=user.user_name,
        created_at=user.created_at,
    )

    return res

@router.get("/{user_id}", response_model=UserResponse, dependencies=[Depends(auth)])
async def get_user(user_id: UUID, service: UserService = Depends(get_user_service)):
    user = await service.get_user(user_id)

    res = UserResponse(
        id = user.id,
        user_name = user.user_name,
        created_at = user.created_at,
    )

    return res


@router.patch("/me", response_model=UserResponse)
async def update_user(data: UserUpdate, current_user_id: UUID = Depends(auth), service: UserService = Depends(get_user_service)):
    user = await service.update_user(
        user_id=current_user_id,
        user_name=data.user_name,
        old_password=data.old_password,
        new_password=data.new_password,
    )

    res = UserResponse(
        id=user.id,
        user_name=user.user_name,
        created_at=user.created_at,
    )

    return res


@router.delete("/me")
async def delete_user(current_user_id: UUID = Depends(auth), service: UserService = Depends(get_user_service)):
    await service.delete_user(current_user_id)

    return {"detail": "user deleted"}