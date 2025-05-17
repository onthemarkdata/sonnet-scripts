import duckdb
from minio import Minio

def setup_duckdb_minio_connection():
    """Configure DuckDB connection to MinIO and use persistent database."""
    con = duckdb.connect('/apps/my_database.duckdb')  # <-- Explicit persistent database file
    con.execute("INSTALL httpfs;")
    con.execute("LOAD httpfs;")
    con.execute("""
        SET s3_endpoint='minio:9000';
        SET s3_access_key_id='admin';
        SET s3_secret_access_key='password';
        SET s3_use_ssl=false;
        SET s3_url_style='path';
    """)
    return con
