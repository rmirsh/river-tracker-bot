from functools import cache

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    db_url: str = Field(env="DB_URL")
    token: str = Field(env="TOKEN")
    delay: int = Field(env="DELAY", default=30 * 60)
    postgres_host_auth_method: str = Field(env="POSTGRES_HOST_AUTH_METHOD", default="")
    postgres_user: str = Field(env="POSTGRES_USER")
    postgres_password: str | None = Field(env="POSTGRES_PASSWORD")
    postgres_db: str = Field(env="POSTGRES_DB", default="")

    model_config = SettingsConfigDict(env_file=".env_prod", env_file_encoding="utf-8")


@cache
def get_settings() -> Settings:
    """Return an instance of Settings.

    Returns:
        Settings: An instance of the Settings class.
    """

    return Settings()


settings = get_settings()
