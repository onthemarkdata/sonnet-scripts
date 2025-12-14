import os


# PostgreSQL Configuration
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_HOST = os.getenv("DB_HOST", "pgduckdb")
DB_PORT = os.getenv("DB_PORT", 5432)

# MinIO Configuration
MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "minio:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "admin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "password")
MINIO_USE_SSL = os.getenv("MINIO_USE_SSL", "false").lower() == "true"
MINIO_DEFAULT_BUCKET = os.getenv("MINIO_DEFAULT_BUCKET", "postgres-data")

# DuckDB Configuration
DUCKDB_PATH = os.getenv("DUCKDB_PATH", "/apps/my_database.duckdb")

# Claims Data Configuration
CLAIMS_URL = os.getenv(
    "CLAIMS_URL",
    "http://downloads.cms.gov/files/DE1_0_2008_to_2010_Carrier_Claims_Sample_2A.zip",
)
CLAIMS_ZIP_FILE = os.getenv("CLAIMS_ZIP_FILE", "claims.zip")
CLAIMS_CSV_FILE = os.getenv("CLAIMS_CSV_FILE", "claims.csv")
CLAIMS_ORIGINAL_CSV = os.getenv(
    "CLAIMS_ORIGINAL_CSV", "DE1_0_2008_to_2010_Carrier_Claims_Sample_2A.csv"
)
