import duckdb
from minio import Minio

def setup_duckdb_to_minio():
    """Set up DuckDB with MinIO (S3-compatible) connection."""
    duckdb.sql("INSTALL httpfs;")
    duckdb.sql("LOAD httpfs;")

    duckdb.sql("""
        SET s3_endpoint='minio:9000';
        SET s3_access_key_id='admin';
        SET s3_secret_access_key='password';
        SET s3_use_ssl=false;
        SET s3_url_style='path';
    """)

def create_bucket_if_not_exists(bucket_name):
    """Create MinIO bucket if it doesn't already exist."""
    client = Minio(
        endpoint="minio:9000",
        access_key="admin",
        secret_key="password",
        secure=False,
    )

    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)
        print(f"Bucket '{bucket_name}' created.")
    else:
        print(f"Bucket '{bucket_name}' already exists.")

def export_csv_to_minio():
    """Export CSV directly to MinIO via DuckDB."""
    bucket_name = 'postgres-data'
    create_bucket_if_not_exists(bucket_name)

    duckdb.sql(f"""
        COPY (
            SELECT * FROM read_csv_auto('/apps/raw_claims.csv')
        ) TO 's3://{bucket_name}/raw_claims.parquet' (FORMAT PARQUET);
    """)
    print("CSV successfully converted and uploaded to MinIO.")

def main():
    setup_duckdb_to_minio()
    export_csv_to_minio()

if __name__ == "__main__":
    main()
