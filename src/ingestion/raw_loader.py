# src/ingestion/raw_loader.py

import json
import boto3
from botocore.exceptions import ClientError
from src.logger.logging_config import logger


class RawLoader:
    def __init__(self, config: dict):
        self.config = config
        self.s3 = boto3.client("s3", region_name=config["REGION"])
        self.bucket = config["S3_INPUT_BUCKET"]
        self.prefix = config["S3_INPUT_PREFIX"]

    def load_from_s3(self, filename: str) -> dict:
        """Load raw JSON file from S3."""
        key = f"{self.prefix}{filename}.json"

        logger.info("loading file from S3", bucket=self.bucket, key=key)

        try:
            response = self.s3.get_object(Bucket=self.bucket, Key=key)
            text = response["Body"].read().decode("utf-8")
            data = json.loads(text)

            logger.info("file loaded successfully", key=key)
            return data

        except ClientError as e:
            logger.error("s3 read error", error=str(e), bucket=self.bucket, key=key)
            raise

        except json.JSONDecodeError as e:
            logger.error("invalid json format", error=str(e), key=key)
            raise
