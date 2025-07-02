"""Application configuration using pydantic-settings."""

from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict
from typing import Optional

class Settings(BaseSettings):
    """Application settings with environment variable support."""
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Application
    APP_NAME: str = Field(default="LinkedIn Clone")
    APP_DESCRIPTION: str = Field(default="Professional Networking Platform")
    APP_VERSION: str = Field(default="1.0.0")
    DEBUG: bool = Field(default=False)
    
    # Server
    HOST: str = Field(default="0.0.0.0")
    PORT: int = Field(default=8000)
    API_PREFIX: str = Field(default="/api")
    
    # Security
    SECRET_KEY: str = Field(default="your-secret-key-change-in-production")
    ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30)
    
    # Database
    DATABASE_URL: str = Field(default="sqlite:///./data/linkedin_clone.db")
    
    # File uploads
    UPLOAD_DIR: str = Field(default="app/static/uploads")
    MAX_FILE_SIZE: int = Field(default=10 * 1024 * 1024)  # 10MB
    ALLOWED_EXTENSIONS: list = Field(default=["jpg", "jpeg", "png", "gif"])

settings = Settings()

__all__ = ["settings"]