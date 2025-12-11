# src/orchestration/ingestion_orchestrator.py
from src.ingestion.raw_loader import RawLoader
from src.schemas.raw_input_schema import RawInputSchema
from src.utils.id_generator import trace_id_generator
from src.canonicalizer.name_mapper import NameMapper
from src.canonicalizer.unit_conversion import UnitConversionEngine
from src.qc.quality_check import QCEngine
from src.repository.sample_repository import SampleRepository

from src.logger.logging_config import logger


class IngestionOrchestrator:
    def __init__(self, config):
        self.config = config
        self.loader = RawLoader(config)
        self.canonicalizer = NameMapper(config)
        self.unit_converter = UnitConversionEngine(config)
        self.qc_engine = QCEngine(config)
        self.sample_repo = SampleRepository(config)

    def run(self, filename: str):

        raw_data = self.loader.load_from_s3(filename)

        # 2. Validate payload
        validated_model = RawInputSchema(**raw_data)
        validated = validated_model.dict()

        # 3. Attach trace_id
        validated["trace_id"] = trace_id_generator()

        # 4. Canonicalize biomarker names
        biomarkers = validated["biomarkers"]
        canonical_biomarkers = []

        for raw_name, value in biomarkers.items():
            canonical_name = self.canonicalizer.map_name(raw_name)

            if canonical_name is None:
                # DROP biomarker cleanly
                logger.warning("biomarker dropped (no canonical mapping found)", raw_name=raw_name)
                continue
            value['canonical_name'] = canonical_name
            canonical_biomarkers.append(value)

        validated["biomarkers"] = canonical_biomarkers

        # 5. Unit conversion (VALUE + UNIT ONLY)
        normalized_biomarkers = self.unit_converter.normalize_all(canonical_biomarkers)
        validated["biomarkers"] = normalized_biomarkers

        # 6. QC VALIDATION
        validated["biomarkers"], qc_summary = self.qc_engine.run_qc(validated["biomarkers"])
        validated["qc_summary"] = qc_summary

        # 7. load the sample
        self.sample_repo.save_structured_sample(validated)

        logger.info("payload validated successfully", user_id=validated['user_id'], trace_id=validated['trace_id'], sample_id=validated['sample_id'])

        return validated
