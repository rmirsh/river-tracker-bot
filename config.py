from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_URL: str = "postgresql+asyncpg://kamilayupov:@localhost/test"
    TOKEN: str = "6744838238:AAHXxj5NFPBsBw9msk_N86dkJ0jN5-qz0hI"


settings = Settings()
