import os
from functools import lru_cache
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration."""

    project_name: str = "A cool timers with a Face"
    debug: bool = Field(default=False, env="DEBUG")
    database_url: str = Field(default="postgresql://user:password@localhost/timer", env="DATABASE_URL")
    jwt_secret: str = Field(default="dev-secret-key-change-in-production", env="JWT_SECRET")
    cors_origins: list[str] = Field(default=["http://localhost:5173", "http://localhost:3000"], env="CORS_ORIGINS")
    api_version: str = "v1"
    environment: str = Field(default="development", env="ENVIRONMENT")

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached application settings."""
    return Settings()
