# src/orchestration/ingestion_orchestrator.py

from src.logger.logging_config import logger


class IngestionOrchestrator:
    def __init__(self, config):
        self.config = config
#         self.loader = RawLoader(config)
#         self.canonicalizer = Canonicalizer(config)
#         self.qc_engine = QCEngine(config)
#         self.builder = PayloadBuilder(config)
#
#     def run(self, filename: str):
#         raw = self.loader.load_and_validate(filename)
#         canonical = self.canonicalizer.apply(raw)
#         qc = self.qc_engine.run(canonical)
#         final_payload = self.builder.build(canonical, qc)
#         return final_payload
