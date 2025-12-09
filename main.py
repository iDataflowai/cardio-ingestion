# main.py

from src.config.config_loader import get_ingestion_config
from src.orchestration.ingestion_orchestrator import IngestionOrchestrator
from src.logger.logging_config import logger

from src.ingestion.raw_loader import RawLoader
from src.orchestration.ingestion_orchestrator import IngestionOrchestrator


def run_ingestion(filename: str):
    logger.info("starting ingestion pipeline", filename=filename)

    # 1. Load config
    config = get_ingestion_config()

    # 2. Load file from S3
    loader = RawLoader(config)
    raw_json = loader.load_from_s3(filename)

    # 3. Run validation
    orchestrator = IngestionOrchestrator(config)
    validated_payload = orchestrator.run(raw_json)

    print(f"validated_payload: {validated_payload}")
    logger.info("ingestion step complete", validated=validated_payload)
    print("done")


if __name__ == '__main__':
    run_ingestion('user_12345.json')
