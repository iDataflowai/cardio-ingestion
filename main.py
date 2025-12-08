# main.py

from src.config.config_loader import get_ingestion_config
from src.orchestration.ingestion_orchestrator import IngestionOrchestrator
from src.logger.logging_config import logger


def run_ingestion(filename: str):
    """
    Entry point for ingestion pipeline.
    Loads config once and orchestrates full ingestion process.
    """

    logger.info("starting ingestion pipeline", filename=filename)

    # ---------------------------------------------------------
    # 1. Load config only ONCE
    # ---------------------------------------------------------
    config = get_ingestion_config()
    logger.info("config loaded successfully", env=config.get("RUNTIME_ENV"))
    # logger.info("config loaded successfully", env=config.get("RUNTIME_ENV"))

    # ---------------------------------------------------------
    # 2. Create orchestrator with config
    # ---------------------------------------------------------
    orchestrator = IngestionOrchestrator(config)
    data = orchestrator.run('user_12345.json')
    print(data)
    # ---------------------------------------------------------
    # 3. Run ingestion
    # ---------------------------------------------------------


if __name__ == '__main__':
    run_ingestion('abc.json')
