from uuid import UUID
from sqlalchemy import delete, select, update
from sqlalchemy.exc import IntegrityError
from ..models.url import URL
from sqlalchemy.ext.asyncio import AsyncSession

class URLRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_url(self, user_id: UUID, original_url: str, short_code: str) -> URL:
        db_url = URL(user_id=user_id, original_url=original_url, short_code=short_code)
        self.db.add(db_url)
        try:
            await self.db.commit()
        except IntegrityError:
            await self.db.rollback()
            raise
        await self.db.refresh(db_url)
        return db_url

    async def get_url(self, url_id: UUID) -> URL | None:
        result = await self.db.execute(select(URL).where(URL.id == url_id))
        return result.scalar_one_or_none()

    async def get_url_by_code(self, short_code: str) -> URL | None:
        result = await self.db.execute(select(URL).where(URL.short_code == short_code))
        return result.scalar_one_or_none()

    async def get_user_urls(self, user_id: UUID, limit: int, offset: int) -> list[URL]:
        result = await self.db.execute(select(URL).where(URL.user_id == user_id).limit(limit).offset(offset))
        return result.scalars().all()

    async def update_url(self, url_id: UUID, original_url: str | None = None, short_code: str | None = None) -> URL | None:
        values = {}
        if original_url is not None:
            values["original_url"] = original_url
        if short_code is not None:
            values["short_code"] = short_code
        if not values:
            return self.get_url(url_id)
        try:
            self.db.execute(update(URL).where(URL.id == url_id).values(**values))
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            raise
        return self.get_url(url_id)

    async def delete_url(self, url_id: UUID) -> bool:
        result = await self.db.execute(delete(URL).where(URL.id == url_id))
        await self.db.commit()
        return result.rowcount > 0

    async def add_click(self, url_id: UUID) -> bool:
        result = await self.db.execute(update(URL).where(URL.id == url_id).values(clicks=URL.clicks + 1))
        await self.db.commit()
        return result.rowcount > 0