from uuid import UUID

from ..errors import InvalidCredentialsError, AlreadyExistsError, NotFoundError
from ..models.user import User
from ..repositories.user import UserRepository
from ..utils.password import PasswordHasher


class UserService:
    def __init__(
        self,
        repository: UserRepository,
        password_hasher: PasswordHasher,
    ):
        self.repository = repository
        self.password_hasher = password_hasher



    async def get_user(self, user_id: UUID) -> User:
        user = await self.repository.get_user(user_id)

        if user is None:
            raise NotFoundError()

        return user

    async def get_user_by_name(self, user_name: str) -> User:
        user = await self.repository.get_user_by_name(user_name)

        if user is None:
            raise NotFoundError()

        return user

    async def get_users(self, limit: int, offset: int) -> list[User]:
        return await self.repository.get_users(limit, offset)

    async def update_user(self, user_id: UUID, user_name: str | None = None, old_password: str | None = None, new_password: str | None = None) -> User:
        user = await self.repository.get_user(user_id)

        if user is None:
            raise NotFoundError()

        if user_name is not None and user_name != user.user_name:
            existing_user = await self.repository.get_user_by_name(user_name)

            if existing_user is not None:
                raise AlreadyExistsError()

        password_hash = None

        if new_password is not None:
            if old_password is None:
                raise InvalidCredentialsError()

            if not self.password_hasher.verify(
                old_password,
                user.password_hash,
            ):
                raise InvalidCredentialsError()

            password_hash = self.password_hasher.hash(new_password)

        updated_user = await self.repository.update_user(
            user_id=user_id,
            user_name=user_name,
            password_hash=password_hash,
        )

        if updated_user is None:
            raise NotFoundError()

        return updated_user

    async def delete_user(self, user_id: UUID) -> None:
        deleted = await self.repository.delete_user(user_id)

        if not deleted:
            raise NotFoundError()