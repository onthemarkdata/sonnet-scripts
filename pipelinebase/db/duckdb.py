import duckdb

import config
from logging_config import setup_logging

logger = setup_logging(__name__)


def setup_duckdb_minio_connection():
    """Configure DuckDB connection to MinIO and use persistent database."""
    con = duckdb.connect(config.DUCKDB_PATH)
    con.execute("INSTALL httpfs;")
    con.execute("LOAD httpfs;")
    con.execute(f"""
        SET s3_endpoint='{config.MINIO_ENDPOINT}';
        SET s3_access_key_id='{config.MINIO_ACCESS_KEY}';
        SET s3_secret_access_key='{config.MINIO_SECRET_KEY}';
        SET s3_use_ssl={'true' if config.MINIO_USE_SSL else 'false'};
        SET s3_url_style='path';
    """)
    logger.debug("DuckDB MinIO connection established")
    return con
