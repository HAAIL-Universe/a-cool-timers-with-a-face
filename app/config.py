from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration from environment variables."""
    
    cors_origins: str = "http://localhost:3000,http://localhost:5173"
    default_duration_seconds: int = 30
    jwt_secret: str = "dev-secret-key"
    database_url: str = "postgresql://user:password@localhost:5432/timers"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
