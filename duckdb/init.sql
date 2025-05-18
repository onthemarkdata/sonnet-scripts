-- Install and load HTTPFS extension for MinIO access
INSTALL httpfs;
LOAD httpfs;

-- Configure MinIO connection
SET s3_access_key_id='admin';
SET s3_secret_access_key='password';
SET s3_endpoint='minio:9000';
SET s3_use_ssl=false;
SET s3_url_style='path';