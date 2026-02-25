from pydantic_settings import BaseSettings


DEFAULT_DURATION_SECONDS = 60
CORS_ORIGINS = ["*"]


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    default_duration_seconds: int = DEFAULT_DURATION_SECONDS
    cors_origins: list[str] = CORS_ORIGINS

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


_settings: Settings | None = None


def get_settings() -> Settings:
    """Get or create the global settings instance."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings
