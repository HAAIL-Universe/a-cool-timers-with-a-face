from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application configuration from environment variables."""
    
    cors_origins: str = "*"
    default_duration_seconds: int = 60
    jwt_secret: str = "dev-secret-key"
    database_url: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = False


_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get or create the global Settings instance."""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings


settings = get_settings()

CORS_ORIGINS = settings.cors_origins
DEFAULT_DURATION_SECONDS = settings.default_duration_seconds
