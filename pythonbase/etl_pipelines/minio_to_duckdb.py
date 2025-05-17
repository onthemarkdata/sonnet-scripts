from .db_utils import setup_duckdb_minio_connection

def import_minio_to_duckdb(con, bucket_name, parquet_file, duckdb_table):
    minio_url = f"s3://{bucket_name}/{parquet_file}"
    con.execute(f"""
        CREATE TABLE IF NOT EXISTS {duckdb_table} AS
        SELECT * FROM read_parquet('{minio_url}');
    """)
    print(f"Successfully imported '{minio_url}' into DuckDB table '{duckdb_table}'.")

def main():
    con = setup_duckdb_minio_connection()
    bucket_name = 'postgres-data'
    parquet_file = 'raw_claims.parquet'
    duckdb_table = 'raw_claims'
    
    import_minio_to_duckdb(con, bucket_name, parquet_file, duckdb_table)
    con.close()

if __name__ == "__main__":
    main()