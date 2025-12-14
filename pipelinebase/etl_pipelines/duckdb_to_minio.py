import config
from db.duckdb import setup_duckdb_minio_connection
from db.minio import create_bucket_if_not_exists
from logging_config import setup_logging

logger = setup_logging(__name__)


def export_csv_to_minio(con):
    """Export CSV data to MinIO as Parquet using DuckDB."""
    bucket_name = config.MINIO_DEFAULT_BUCKET
    create_bucket_if_not_exists(bucket_name)

    con.execute(f"""
        COPY (
            SELECT * FROM read_csv_auto('/apps/raw_claims.csv')
        ) TO 's3://{bucket_name}/raw_claims.parquet' (FORMAT PARQUET);
    """)
    logger.info("CSV successfully converted and uploaded to MinIO.")


def main():
    con = setup_duckdb_minio_connection()
    export_csv_to_minio(con)
    con.close()


if __name__ == "__main__":
    main()
