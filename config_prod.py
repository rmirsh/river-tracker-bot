from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_URL: str
    TOKEN: str


settings = Settings()
