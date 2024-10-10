from functools import cache

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, BaseModel, PostgresDsn


class GeneralConfig(BaseModel):
    is_prod: bool


class BotConfig(BaseModel):
    token: str
    test_token: str


class ParserConfig(BaseModel):
    delay: int = 30 * 60


class DatabaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )
    parser: ParserConfig = ParserConfig()
    db: DatabaseConfig
    bot: BotConfig
    general: GeneralConfig


@cache
def get_settings() -> Settings:
    """Return an instance of Settings.

    Returns:
        Settings: An instance of the Settings class.
    """

    return Settings()


settings = get_settings()

if __name__ == "__main__":
    print(settings)
