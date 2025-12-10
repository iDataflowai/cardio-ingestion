# src/canonicalizer/name_mapper.py

import psycopg2
from psycopg2.extras import RealDictCursor
from src.logger.logging_config import logger


class NameMapper:
    """
    Maps raw biomarker names to canonical names using the
    cis_biomarker_alias_map table in RDS PostgreSQL.
    """

    def __init__(self, config):
        self.config = config

        # RDS connection details
        self.host = config["RDS_HOST"]
        self.port = config["RDS_PORT"]
        self.db = config["RDS_DB"]
        self.user = config["RDS_USER"]
        self.password = config["RDS_PASSWORD"]

        self.conn = psycopg2.connect(
            host=self.host,
            port=self.port,
            database=self.db,
            user=self.user,
            password=self.password,
            cursor_factory=RealDictCursor
        )

    def map_name(self, raw_name: str) -> str:
        """
        Return the canonical name for the raw alias.
        If no mapping found, return None.
        """

        raw_clean = raw_name.strip().lower()

        query = """
            SELECT canonical_name
            FROM cis_biomarker_alias_map
            WHERE LOWER(alias_name) = %s
            AND is_active = TRUE
            LIMIT 1;
        """

        with self.conn.cursor() as cur:
            cur.execute(query, (raw_clean,))
            result = cur.fetchone()

        if result:
            canonical = result["canonical_name"]
            logger.info("canonical name matched", raw_name=raw_name, canonical_name=canonical)
            return canonical

        # No match found
        logger.warn("no canonical match found", raw_name=raw_name)
        return None

    def close(self):
        if self.conn:
            self.conn.close()
