# main.py

from src.config.config_loader import get_ingestion_config
from src.logger.logging_config import logger
from src.orchestration.ingestion_orchestrator import IngestionOrchestrator


def run_ingestion(filename: str):
    logger.info("starting ingestion pipeline", filename=filename)

    # 1. Load config
    config = get_ingestion_config()

    # 2. Run validation
    orchestrator = IngestionOrchestrator(config)
    orchestrator.run(filename)

    logger.info("ingestion step complete")


if __name__ == '__main__':
    run_ingestion('user_12345.json')
