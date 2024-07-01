from functools import cache

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    DB_URL: str = Field(env="DB_URL")
    TOKEN: str = Field(env="TOKEN")
    DELAY: int = Field(env="DELAY", default=30 * 60)
    POSTGRES_HOST_AUTH_METHOD: str = Field(env="POSTGRES_HOST_AUTH_METHOD", default="")
    POSTGRES_USER: str = Field(env="POSTGRES_USER")
    POSTGRES_PASSWORD: str | None = Field(env="POSTGRES_PASSWORD")
    POSTGRES_DB: str = Field(env="POSTGRES_DB", default="")

    model_config = SettingsConfigDict(env_file=".env_prod", env_file_encoding="utf-8")


@cache
def get_settings() -> Settings:
    """Return an instance of Settings.

    Returns:
        Settings: An instance of the Settings class.
    """

    return Settings()


settings = get_settings()
