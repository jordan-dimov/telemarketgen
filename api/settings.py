from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "AI Telemarketing API"
    session_secret: str = "super-secret!"
    sqlite_url: str = "sqlite:///./telemarket.db"
    output_folder: str = "samples"
    openai_api_key: str | None = None
    anthropic_api_key: str | None = None


settings = Settings()
