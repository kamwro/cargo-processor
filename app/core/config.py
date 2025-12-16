from functools import lru_cache
from typing import List, Optional

from pydantic import AnyHttpUrl, Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_key: Optional[str] = Field(default=None, alias="API_KEY")
    api_token: Optional[str] = Field(default=None, alias="API_TOKEN")
    backend_base_url: Optional[AnyHttpUrl] = Field(default=None, alias="BACKEND_BASE_URL")
    allowed_origins: List[str] = Field(default_factory=list, alias="ALLOWED_ORIGINS")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
