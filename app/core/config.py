from functools import lru_cache

from pydantic import AnyHttpUrl, Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_key: str | None = Field(default=None, alias="API_KEY")
    api_token: str | None = Field(default=None, alias="API_TOKEN")
    backend_base_url: AnyHttpUrl | None = Field(default=None, alias="BACKEND_BASE_URL")
    allowed_origins: list[str] = Field(default_factory=list, alias="ALLOWED_ORIGINS")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
