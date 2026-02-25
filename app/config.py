from pydantic_settings import BaseSettings
from typing import Literal


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    cors_origins: list[str] = ["http://localhost:3000", "http://localhost:5173"]
    default_duration_seconds: int = 30
    jwt_secret: str = "dev-secret-change-in-production"
    environment: Literal["development", "production"] = "development"

    class Config:
        env_file = ".env"
        case_sensitive = False

    def get_cors_origins(self) -> list[str]:
        """Parse CORS_ORIGINS from comma-separated env string."""
        if isinstance(self.cors_origins, str):
            return [origin.strip() for origin in self.cors_origins.split(",")]
        return self.cors_origins


settings = Settings()
