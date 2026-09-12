import logging

from fastapi import Request
from fastapi.responses import JSONResponse


logger = logging.getLogger(__name__)


async def recovery_middleware(request: Request, call_next):
    try:
        return await call_next(request)

    except Exception:
        request_id = getattr(request.state, "request_id", None)

        logger.exception(
            "Unhandled exception",
            extra={"request_id": request_id},
        )

        return JSONResponse(
            status_code=500,
            content={
                "detail": "Internal server error",
                "request_id": request_id,
            },
        )