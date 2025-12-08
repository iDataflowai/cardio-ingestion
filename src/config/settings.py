# src/cardio_ingestion/config/settings.py

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """
    Global settings for ingestion pipeline.
    Supports:
    - Local development (.env)
    - AWS Lambda environment variables
    """

    CARDIO_INGESTION_SECRET_NAME: str = "cardio/ingestion/config"
    AWS_SECRET_REGION: str = "us-east-1"
    INGESTION_ENV: str = "dev"   # dev / qa / prod

    class Config:
        env_file = ".env"  # loaded only in local development


@lru_cache()
def get_settings() -> Settings:
    """Load settings once (cached)."""
    return Settings()
