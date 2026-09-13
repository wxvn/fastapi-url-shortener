from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.errors import AppError
from src.routes.users import router as users_router
from src.routes.auth import router as auth_router
from src.routes.url import router as urls_router
from src.routes.redirect import router as redirect_router
from src.middleware import request_id_middleware, recovery_middleware




app = FastAPI()

app.middleware("http")(request_id_middleware)
app.middleware("http")(recovery_middleware)


@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )


app.include_router(users_router)
app.include_router(auth_router)
app.include_router(urls_router)
app.include_router(redirect_router)