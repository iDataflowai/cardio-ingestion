# src/qc/qc_engine.py

import psycopg2
from psycopg2.extras import RealDictCursor
from src.logger.logging_config import logger
from src.utils.unit_utils import db_connection


class QCEngine:
    """
    QC Engine performs:
    - missing value validation
    - critical (dominant) biomarker validation per bucket
    - per-biomarker QC tagging
    - overall QC summary computation

    Data source:
        cis_biomarker_weightage_mapping
    """

    def __init__(self, config):
        self.config = config
        self.conn = db_connection(config)

        # Load mapping from DB
        (
            self.bucket_to_dominant,
            self.all_expected_biomarkers
        ) = self._load_biomarker_rules()

    # ----------------------------------------------------------------------
    # Load bucket → dominant biomarkers AND global expected biomarkers
    # ----------------------------------------------------------------------
    def _load_biomarker_rules(self):
        query = """
            SELECT biomarker_name, bucket_name, role
            FROM cis_biomarker_weightage_mapping;
        """

        bucket_to_dominant = {}
        all_expected = set()

        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query)
            rows = cur.fetchall()

        for row in rows:
            biomarker = row["biomarker_name"]
            bucket = row["bucket_name"]
            role = row["role"]

            all_expected.add(biomarker)

            if role == "Dominant":
                bucket_to_dominant.setdefault(bucket, set()).add(biomarker)

        logger.info("QC rules loaded",
                    buckets=len(bucket_to_dominant),
                    expected_biomarkers=len(all_expected))

        return bucket_to_dominant, all_expected

    # ----------------------------------------------------------------------
    # QC evaluation for a full sample
    # ----------------------------------------------------------------------
    def run_qc(self, normalized_biomarkers: list):
        """
        normalized_biomarkers: list of dicts after unit conversion
        Returns:
            updated biomarker list + qc_summary (dict)
        """

        qc_summary = {
            "missing_critical_markers": False,
            "missing_critical_biomarkers": [],
            "total_invalid_markers": 0,
            "implausible_markers": [],      # future expansion
            "overall_status": "valid"
        }

        # ----------------------------------------------------------
        # Step 1: Create quick lookup of biomarkers present in payload
        # ----------------------------------------------------------
        present_values = {
            sample["canonical_name"]: sample
            for sample in normalized_biomarkers
        }

        present_names = set(present_values.keys())

        # ----------------------------------------------------------
        # Step 2: Mark missing/invalid biomarkers
        # ----------------------------------------------------------
        for sample in normalized_biomarkers:
            name = sample["canonical_name"]
            value = sample["normalized_value"]

            if value is None or value == "" or (sample["is_range"] and value == {}):
                sample["qc_check"] = "invalid"
                qc_summary["total_invalid_markers"] += 1
            else:
                sample["qc_check"] = "valid"

        # ----------------------------------------------------------
        # Step 3: Validate dominant biomarkers per bucket
        # ----------------------------------------------------------
        for bucket, dom_set in self.bucket_to_dominant.items():
            for biomarker in dom_set:
                # If biomarker missing entirely
                if biomarker not in present_names:
                    qc_summary["missing_critical_markers"] = True
                    qc_summary["missing_critical_biomarkers"].append({
                        "biomarker": biomarker,
                        "bucket": bucket,
                        "reason": "not_collected"
                    })
                    continue

                # If biomarker exists but invalid
                s = present_values[biomarker]
                if s["qc_check"] != "valid":
                    qc_summary["missing_critical_markers"] = True
                    qc_summary["missing_critical_biomarkers"].append({
                        "biomarker": biomarker,
                        "bucket": bucket,
                        "reason": "value_invalid"
                    })

        # ----------------------------------------------------------
        # Step 4: Determine final overall_status
        # ----------------------------------------------------------
        if qc_summary["missing_critical_markers"]:
            qc_summary["overall_status"] = "invalid"
        else:
            qc_summary["overall_status"] = "valid"

        return normalized_biomarkers, qc_summary
