from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine


from .config import settings


engine = create_async_engine(settings.database_url)

SessionLocal = async_sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with SessionLocal() as db:
        yield db


