from uuid import UUID

from ..models.url import URL

from ..errors import NotFoundError, ForbiddenError
from ..repositories.url import URLRepository
from ..utils.short_code import ShortCodeGenerator


class UrlService:
    def __init__(self, repository: URLRepository, generator: ShortCodeGenerator):
        self.repository = repository
        self.generator = generator

    async def create_url(self, user_id: UUID, original_url: str) -> URL:
        short_code = self.generator.generate()
        return await self.repository.create_url(user_id, original_url, short_code)

    async def get_url(self, url_id: UUID) -> URL:
        url = await self.repository.get_url(url_id)
        if url is None:
            raise NotFoundError()
        return url

    async def get_url_by_code(self, short_code: str) -> URL:
        url = await self.repository.get_url_by_code(short_code)
        if url is None:
            raise NotFoundError()
        return url

    async def get_user_urls(self, user_id: UUID, limit: int, offset: int) -> list[URL]:
        return await self.repository.get_user_urls(user_id, limit, offset)

    async def update_url(self, url_id: UUID, user_id: UUID, original_url: str | None = None, short_code: str | None = None) -> URL:
        url = await self.repository.get_url(url_id)

        if url is None:
            raise NotFoundError()

        if url.user_id != user_id:
            raise ForbiddenError()

        url_update = await self.repository.update_url(url_id, original_url, short_code)
        if url is None:
            raise NotFoundError()
        return url_update

    async def delete_url(self, url_id: UUID, user_id: UUID) -> None:
        url = await self.repository.get_url(url_id)

        if url is None:
            raise NotFoundError()

        if url.user_id != user_id:
            raise ForbiddenError()

        deleted = await self.repository.delete_url(url_id)

        if not deleted:
            raise NotFoundError()

    async def add_click(self, url_id: UUID) -> None:
        added = await self.repository.add_click(url_id)
        if not added:
            raise NotFoundError()