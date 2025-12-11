import config
from db.duckdb import setup_duckdb_minio_connection
from db.validation import validate_identifier, validate_s3_path
from logging_config import setup_logging

logger = setup_logging(__name__)


def import_minio_to_duckdb(con, bucket_name, parquet_file, duckdb_table):
    """Import Parquet data from MinIO into a DuckDB table."""
    validate_s3_path(bucket_name, parquet_file)
    validate_identifier(duckdb_table, "table name")

    minio_url = f"s3://{bucket_name}/{parquet_file}"
    con.execute(f"""
        CREATE TABLE IF NOT EXISTS {duckdb_table} AS
        SELECT * FROM read_parquet('{minio_url}');
    """)
    logger.info(f"Successfully imported '{minio_url}' into DuckDB table '{duckdb_table}'.")


def main():
    con = setup_duckdb_minio_connection()
    bucket_name = config.MINIO_DEFAULT_BUCKET
    parquet_file = "raw_claims.parquet"
    duckdb_table = "raw_claims"

    import_minio_to_duckdb(con, bucket_name, parquet_file, duckdb_table)
    con.close()


if __name__ == "__main__":
    main()
