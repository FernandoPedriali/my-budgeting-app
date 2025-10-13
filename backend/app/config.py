"""Application configuration using Pydantic Settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    APP_NAME: str = "My Budgeting App"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/budgeting_app"

    # API
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_RELOAD: bool = True

    # Frontend
    FRONTEND_HOST: str = "0.0.0.0"
    FRONTEND_PORT: int = 8080

    # CORS
    CORS_ORIGINS: list[str] = [
        "http://localhost:8080",  # Frontend NiceGUI
        "http://localhost:8000",  # API docs
    ]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


# Create global settings instance
settings = Settings()
