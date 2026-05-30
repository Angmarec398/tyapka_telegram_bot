from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    TELEGRAM_BOT_TOKEN: str
    BACKEND_BASE_URL: str = "http://localhost:8000"
    INTERNAL_API_TOKEN: str
    LOG_LEVEL: str = "INFO"


settings = Settings()
