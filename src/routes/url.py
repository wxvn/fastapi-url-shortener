from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from ..middleware import auth
from ..repositories.url import URLRepository
from ..schemas.pagination import Pagination
from ..schemas.url import URLCreate, URLResponse, URLUpdate
from ..services.url import UrlService
from ..utils.short_code import RandomShortCodeGenerator


router = APIRouter(prefix="/urls", tags=["urls"])


def get_url_service(db: AsyncSession = Depends(get_db)) -> UrlService:
    repository = URLRepository(db)
    generator = RandomShortCodeGenerator()

    return UrlService(repository, generator)


@router.post("/", response_model=URLResponse)
async def create_url(data: URLCreate, current_user_id: UUID = Depends(auth), service: UrlService = Depends(get_url_service)):
    url = await service.create_url(
        user_id=current_user_id,
        original_url=data.original_url,
    )

    res = URLResponse(
        id=url.id,
        original_url=url.original_url,
        short_code=url.short_code,
        clicks=url.clicks,
        created_at=url.created_at,
    )

    return res


@router.get("/me", response_model=list[URLResponse])
async def get_user_urls(pagination: Pagination = Depends(), current_user_id: UUID = Depends(auth), service: UrlService = Depends(get_url_service)):
    urls = await service.get_user_urls(
        user_id=current_user_id,
        limit=pagination.limit,
        offset=pagination.offset,
    )

    res = []

    for url in urls:
        res.append(
            URLResponse(
                id=url.id,
                original_url=url.original_url,
                short_code=url.short_code,
                clicks=url.clicks,
                created_at=url.created_at,
            )
        )

    return res


@router.get("/{url_id}", response_model=URLResponse, dependencies=[Depends(auth)])
async def get_url(url_id: UUID, service: UrlService = Depends(get_url_service)):
    url = await service.get_url(url_id)

    res = URLResponse(
        id=url.id,
        original_url=url.original_url,
        short_code=url.short_code,
        clicks=url.clicks,
        created_at=url.created_at,
    )

    return res


@router.get("/code/{short_code}", response_model=URLResponse)
async def get_url_by_code(short_code: str,service: UrlService = Depends(get_url_service)):
    url = await service.get_url_by_code(short_code)

    res = URLResponse(
        id=url.id,
        original_url=url.original_url,
        short_code=url.short_code,
        clicks=url.clicks,
        created_at=url.created_at,
    )

    return res


@router.patch("/{url_id}", response_model=URLResponse)
async def update_url(url_id: UUID, data: URLUpdate, current_user_id: UUID = Depends(auth), service: UrlService = Depends(get_url_service)):
    url = await service.update_url(
        url_id=url_id,
        user_id=current_user_id,
        original_url=data.original_url,
        short_code=data.short_code,
    )

    res = URLResponse(
        id=url.id,
        original_url=url.original_url,
        short_code=url.short_code,
        clicks=url.clicks,
        created_at=url.created_at,
    )

    return res


@router.delete("/{url_id}")
async def delete_url(url_id: UUID, current_user_id: UUID = Depends(auth), service: UrlService = Depends(get_url_service)):
    await service.delete_url(
        url_id=url_id,
        user_id=current_user_id,
    )

    return {"detail": "url deleted"}