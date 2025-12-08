import os
from dotenv import load_dotenv
import boto3
import json

load_dotenv()

SECRET_NAME = os.getenv("CARDIO_INGESTION_SECRET_NAME")
AWS_REGION = os.getenv("AWS_SECRET_REGION")
INGESTION_ENV = os.getenv("INGESTION_ENV", "dev")  # default=dev


def get_ingestion_config():
    client = boto3.client("secretsmanager", region_name=AWS_REGION)
    resp = client.get_secret_value(SecretId=SECRET_NAME)
    config = json.loads(resp["SecretString"])

    # attach runtime environment to config
    config["RUNTIME_ENV"] = INGESTION_ENV
    return config


# if __name__ == "__main__":
#     config = get_ingestion_config()
#     print("data ingestion config:", config)
