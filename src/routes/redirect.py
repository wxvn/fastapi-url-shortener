from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..repositories.url import URLRepository
from ..services.url import UrlService
from ..utils.short_code import RandomShortCodeGenerator


router = APIRouter(tags=["redirect"])


def get_url_service(db: AsyncSession = Depends(get_db)) -> UrlService:
    repository = URLRepository(db)
    generator = RandomShortCodeGenerator()

    return UrlService(repository, generator)


@router.get("/{short_code}")
async def redirect_url(short_code: str, service: UrlService = Depends(get_url_service)):
    url = await service.get_url_by_code(short_code)
    original_url = url.original_url
    await service.add_click(url.id)
    return RedirectResponse(original_url)