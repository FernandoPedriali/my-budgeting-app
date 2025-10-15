"""Frontend configuration settings."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Frontend application settings loaded from environment variables.

    Only loads variables needed by the frontend.
    Ignores backend-specific variables from .env file.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",  # 🔧 MUDANÇA: Ignora variáveis extras (backend vars)
    )

    # Frontend server settings
    FRONTEND_HOST: str = Field(default="0.0.0.0", description="Frontend host address")
    FRONTEND_PORT: int = Field(default=8080, description="Frontend port")

    # Backend API settings (where frontend will make requests)
    BACKEND_HOST: str = Field(default="localhost", description="Backend API host")
    BACKEND_PORT: int = Field(default=8000, description="Backend API port")

    @property
    def backend_url(self) -> str:
        """Get the full backend API URL."""
        return f"http://{self.BACKEND_HOST}:{self.BACKEND_PORT}"


# Global settings instance
settings = Settings()
