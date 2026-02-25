from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""
    database_url: str
    jwt_secret: str
    cors_origins: list[str]

    class Config:
        env_file = ".env"
        case_sensitive = False


def get_settings() -> Settings:
    """Return application settings instance."""
    return Settings()
