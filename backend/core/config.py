"""
Core configuration management for InfraMind.
Loads settings from environment variables and provides centralized config access.
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Gemini Configuration
    gemini_api_key: str
    gemini_model: str = "gemini-2.0-flash-exp"  # Latest experimental model
    
    # Application Settings
    app_env: str = "development"
    debug: bool = True
    log_level: str = "INFO"
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_workers: int = 1
    
    # Processing Limits
    max_file_size_mb: int = 10
    max_context_length: int = 100000
    request_timeout_seconds: int = 30
    
    # Cache Settings
    enable_cache: bool = True
    cache_ttl_seconds: int = 3600
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    @property
    def max_file_size_bytes(self) -> int:
        """Convert MB to bytes for file size validation."""
        return self.max_file_size_mb * 1024 * 1024
    
    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.app_env.lower() == "production"


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    Uses lru_cache to ensure settings are loaded only once.
    """
    return Settings()


# Export for easy imports
settings = get_settings()
