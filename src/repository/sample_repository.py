# src/repository/sample_repository.py

import json
from src.utils.unit_utils import db_connection
from src.logger.logging_config import logger


class SampleRepository:

    def __init__(self, config):
        self.config = config
        self.conn = db_connection(config)

    def save_structured_sample(self, sample: dict):
        """
        Inserts the final structured CIS envelope into structured_biomarker_samples.
        """
        sample_id = sample['sample_id']
        user_id = sample['user_id']
        trace_id = sample['trace_id']
        qc_overall_status = sample['qc_summary']['overall_status']
        version = 'v1.0'

        query = """
            INSERT INTO structured_biomarker_samples 
            (
                sample_id, user_id, trace_id,
                structured_payload, version, qc_overall_status
            )
            VALUES (%s, %s, %s, %s::jsonb, %s, %s)
            ON CONFLICT (sample_id) DO UPDATE SET
                structured_payload = EXCLUDED.structured_payload,
                qc_overall_status  = EXCLUDED.qc_overall_status,
                version            = EXCLUDED.version;
        """

        try:
            with self.conn.cursor() as cur:
                cur.execute(
                    query,
                    (
                        sample_id,
                        user_id,
                        trace_id,
                        json.dumps(sample),
                        version,
                        qc_overall_status
                    )
                )
            self.conn.commit()

            logger.info(
                "structured sample stored successfully",
                sample_id=sample_id,
                user_id=user_id,
                status=qc_overall_status
            )
            return True

        except Exception as e:
            self.conn.rollback()
            logger.error("failed to save structured sample", error=str(e))
            raise
