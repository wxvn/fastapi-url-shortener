from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "FastAPI url"
    debug: bool = True
    database_url: str
    redis_url: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()