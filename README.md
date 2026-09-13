# FastAPI URL Shortener

URL shortener Python FastAPI.

## Stack

* Python
* FastAPI
* PostgreSQL
* SQLAlchemy
* Redis
* Alembic
* Docker
* uv

## Run

Copy `.env.example` to `.env` and configure the environment variables.

```bash
uv sync
docker compose up -d
uv run alembic upgrade head
uv run uvicorn main:app --reload
```

Swagger: `http://localhost:8000/docs`
