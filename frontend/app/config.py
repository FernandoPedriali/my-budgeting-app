"""Frontend configuration."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Frontend settings."""

    # Application
    APP_NAME: str = "My Budgeting App"

    # Frontend Server
    FRONTEND_HOST: str = "0.0.0.0"
    FRONTEND_PORT: int = 8080

    # Backend API
    API_URL: str = "http://localhost:8000"
    API_BASE_PATH: str = "/api/v1"

    # Theme
    DEFAULT_DARK_MODE: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


# Global settings instance
settings = Settings()
