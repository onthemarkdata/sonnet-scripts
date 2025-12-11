from minio import Minio

import config
from logging_config import setup_logging

logger = setup_logging(__name__)


def get_minio_client():
    """Get a configured MinIO client instance."""
    return Minio(
        endpoint=config.MINIO_ENDPOINT,
        access_key=config.MINIO_ACCESS_KEY,
        secret_key=config.MINIO_SECRET_KEY,
        secure=config.MINIO_USE_SSL,
    )


def create_bucket_if_not_exists(bucket_name):
    """Create a MinIO bucket if it doesn't already exist."""
    client = get_minio_client()
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)
        logger.info(f"Created bucket: {bucket_name}")
    else:
        logger.debug(f"Bucket already exists: {bucket_name}")
