# src/config/config_loader.py

import json
import boto3
from src.config.settings import get_settings
from src.logger.logging_config import logger


def get_ingestion_config() -> dict:
    """
    Loads ingestion configuration:
    1. Load environment variables via Settings
    2. Fetch secret from AWS Secrets Manager
    3. Merge values
    """

    settings = get_settings()

    logger.info("loading ingestion configuration", env=settings.INGESTION_ENV, region=settings.AWS_SECRET_REGION)

    # --------------------------------
    # 1. Load Secrets Manager values
    # --------------------------------
    client = boto3.client("secretsmanager", region_name=settings.AWS_SECRET_REGION)

    secret_response = client.get_secret_value(SecretId=settings.CARDIO_INGESTION_SECRET_NAME)

    secret_config = json.loads(secret_response["SecretString"])

    # --------------------------------
    # 2. Attach runtime environment
    # --------------------------------
    secret_config["RUNTIME_ENV"] = settings.INGESTION_ENV

    logger.info("ingestion config loaded successfully")

    return secret_config
