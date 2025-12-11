# src/utils/unit_utils.py

import psycopg2
from psycopg2 import OperationalError


def db_connection(config):
    """
    Creates a secured, timeout-protected PostgreSQL connection.
    Used by canonicalizer, QC engine, scoring, and orchestration layers.
    """

    try:
        conn = psycopg2.connect(
            host=config["RDS_HOST"],
            port=config["RDS_PORT"],
            dbname=config["RDS_DB"],
            user=config["RDS_USER"],
            password=config["RDS_PASSWORD"],
            connect_timeout=5,      # prevent long hangs
            sslmode="require"       # RDS best practice
        )
        return conn

    except OperationalError as e:
        raise RuntimeError(f"Database connection failed: {str(e)}")
