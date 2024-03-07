from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "AI Telemarketing API"
    sqlite_url: str = "sqlite:///./telemarket.db"


settings = Settings()
