# src/canonicalizer/unit_conversion.py

import psycopg2
from psycopg2.extras import RealDictCursor
from src.logger.logging_config import logger


class UnitConversionEngine:
    """
    Loads unit conversion rules from DB and provides fast normalization.
    Table: cis_unit_conversion
    Columns:
        biomarker_name, unit_from, unit_to, factor, additive_offset, is_active
    """

    def __init__(self, config):
        self.config = config
        self.conn = psycopg2.connect(
            host=config["RDS_HOST"],
            port=config["RDS_PORT"],
            dbname=config["RDS_DB"],
            user=config["RDS_USER"],
            password=config["RDS_PASSWORD"],
            cursor_factory=RealDictCursor
        )

        self.conversion_map = self._load_rules()

    # ----------------------------------------------------------------------
    # Load all active conversion rules from DB
    # ----------------------------------------------------------------------
    def _load_rules(self):
        query = """
            SELECT biomarker_name, unit_from, unit_to, factor, additive_offset
            FROM cis_unit_conversion
            WHERE is_active = TRUE;
        """

        rules = {}

        with self.conn.cursor() as cur:
            cur.execute(query)
            rows = cur.fetchall()

        for row in rows:
            biomarker = row["biomarker_name"].strip().lower()
            unit_from = row["unit_from"].strip().lower()

            rules[(biomarker, unit_from)] = {
                "unit_to": row["unit_to"],
                "factor": float(row["factor"]),
                "offset": float(row["additive_offset"])
            }

        logger.info("unit conversion rules loaded", count=len(rules))
        return rules

    # ----------------------------------------------------------------------
    # Normalize a single biomarker value object
    # biomarker_name: canonical biomarker name
    # biomarker_value: dict with raw_value, raw_unit, is_range, comment
    # ----------------------------------------------------------------------
    def normalize_value(self, biomarker_name: str, biomarker_value: int | float, biomarker_unit: str):
        biomarker_key = biomarker_name.strip().lower()
        raw_unit = biomarker_unit.strip().lower()

        # Look up rule
        rule = self.conversion_map.get((biomarker_key, raw_unit))

        if not rule:
            logger.info("no unit conversion required — keeping raw values", biomarker=biomarker_name, raw_unit=raw_unit)
            return {
                "canonical_name": biomarker_name,
                "normalized_value": biomarker_value,   # unchanged
                "normalized_unit": biomarker_unit,   # unchanged
                "is_range": False
            }

        factor = rule["factor"]
        offset = rule["offset"]
        unit_to = rule["unit_to"]

        # ---------------------------
        # Case 1: single numeric value
        # ---------------------------
        if not biomarker_value["is_range"]:
            raw_value = biomarker_value["raw_value"]

            normalized = raw_value * factor + offset

            return {
                "canonical_name": biomarker_name,
                "normalized_value": normalized,
                "normalized_unit": unit_to,
                "is_range": False
            }

        # ---------------------------
        # Case 2: range value
        # ---------------------------
        raw_range = biomarker_value["raw_value"]

        normalized_range = {
            "min": raw_range["min"] * factor + offset,
            "max": raw_range["max"] * factor + offset,
        }

        return {
            "raw_value": normalized_range,
            "raw_unit": unit_to,
            "is_range": True,
            "comment": biomarker_value.get("comment", "")
        }

    # ----------------------------------------------------------------------
    # Normalize all biomarkers in the validated payload
    # ----------------------------------------------------------------------
    def normalize_all(self, biomarkers: dict):
        normalized_biomarkers = []

        for sample in biomarkers:
            b_name = sample['canonical_name']
            b_val = sample['raw_value']
            b_unit = sample['raw_unit']
            normalized_sample = self.normalize_value(b_name, b_val, b_unit)

            normalized_biomarkers.append(normalized_sample)

        return normalized_biomarkers
