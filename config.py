from functools import cache

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    DB_URL: str = Field(env="DB_URL")
    TOKEN: str = Field(env="TOKEN")
    DELAY: int = Field(env="DELAY", default=30 * 60)

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
