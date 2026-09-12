from uuid import UUID
from sqlalchemy import delete, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.user import User

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, user_name: str, password_hash: str) -> User:
        db_user = User(user_name=user_name, password_hash=password_hash)
        self.db.add(db_user)
        try:
            await self.db.commit()
        except IntegrityError:
            await self.db.rollback()
            raise
        await self.db.refresh(db_user)
        return db_user

    async def get_user(self, user_id: UUID) -> User | None:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_user_by_name(self, user_name: str) -> User | None:
        result = await self.db.execute(
            select(User).where(User.user_name == user_name)
        )
        return result.scalar_one_or_none()

    async def get_users(self, limit: int, offset: int) -> list[User]:
        result = await self.db.execute(
            select(User).order_by(User.id).limit(limit).offset(offset)
        )
        return result.scalars().all()

    async def update_user(self, user_id: UUID, user_name: str | None = None, password_hash: str | None = None) -> User | None:
        values = {}
        if user_name is not None:
            values["user_name"] = user_name
        if password_hash is not None:
            values["password_hash"] = password_hash
        if not values:
            return await self.get_user(user_id)
        try:
            await self.db.execute(update(User).where(User.id == user_id).values(**values))

            await self.db.commit()
        except IntegrityError:
            await self.db.rollback()
            raise

        return await self.get_user(user_id)

    async def delete_user(self, user_id: UUID) -> bool:
        result = await self.db.execute(
            delete(User).where(User.id == user_id)
        )
        await self.db.commit()
        return result.rowcount > 0