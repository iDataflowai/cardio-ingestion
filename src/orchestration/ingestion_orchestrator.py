# src/orchestration/ingestion_orchestrator.py
from src.ingestion.raw_loader import RawLoader
from src.schemas.raw_input_schema import RawInputSchema
from src.utils.id_generator import trace_id_generator
from src.logger.logging_config import logger


class IngestionOrchestrator:
    def __init__(self, config):
        self.config = config
        self.loader = RawLoader(config)
#         self.canonicalizer = Canonicalizer(config)
#         self.qc_engine = QCEngine(config)
#         self.builder = PayloadBuilder(config)

    def run(self, filename: str):
        raw_data = self.loader.load_from_s3(filename)

        validated = RawInputSchema(**raw_data).dict()

        if not validated.get('trace_id'):
            validated['trace_id'] = trace_id_generator()

#         canonical = self.canonicalizer.apply(raw)
#         qc = self.qc_engine.run(canonical)
#         final_payload = self.builder.build(canonical, qc)

        logger.info("payload validated successfully", user_id=validated['user_id'], trace_id=validated['trace_id'], sample_id=validated['sample_id'])

        return validated
