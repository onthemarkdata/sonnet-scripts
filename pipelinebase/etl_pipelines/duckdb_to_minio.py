from .db_utils import setup_duckdb_minio_connection
from minio import Minio

def create_bucket_if_not_exists(bucket_name):
    client = Minio(
        endpoint="minio:9000",
        access_key="admin",
        secret_key="password",
        secure=False,
    )

    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)

def export_csv_to_minio(con):
    bucket_name = 'postgres-data'
    create_bucket_if_not_exists(bucket_name)

    con.execute(f"""
        COPY (
            SELECT * FROM read_csv_auto('/apps/raw_claims.csv')
        ) TO 's3://{bucket_name}/raw_claims.parquet' (FORMAT PARQUET);
    """)
    print("CSV successfully converted and uploaded to MinIO.")

def main():
    con = setup_duckdb_minio_connection()
    export_csv_to_minio(con)
    con.close()

if __name__ == "__main__":
    main()