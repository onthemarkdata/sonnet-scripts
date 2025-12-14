import re


def validate_identifier(name, identifier_type="identifier"):
    """
    Validate that a SQL identifier (table name, column name, etc.) is safe.

    Only allows alphanumeric characters and underscores.
    Raises ValueError if the identifier is invalid.
    """
    if not name:
        raise ValueError(f"{identifier_type} cannot be empty")

    if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', name):
        raise ValueError(
            f"Invalid {identifier_type}: '{name}'. "
            "Only alphanumeric characters and underscores are allowed, "
            "and it must start with a letter or underscore."
        )

    return name


def validate_s3_path(bucket_name, file_path):
    """
    Validate S3/MinIO bucket name and file path.

    Bucket names: lowercase alphanumeric, hyphens, 3-63 chars
    File paths: alphanumeric, underscores, hyphens, forward slashes, dots
    """
    if not bucket_name:
        raise ValueError("Bucket name cannot be empty")

    if not re.match(r'^[a-z0-9][a-z0-9\-]{1,61}[a-z0-9]$', bucket_name):
        raise ValueError(
            f"Invalid bucket name: '{bucket_name}'. "
            "Must be 3-63 characters, lowercase alphanumeric and hyphens only."
        )

    if not file_path:
        raise ValueError("File path cannot be empty")

    if not re.match(r'^[a-zA-Z0-9_\-./]+$', file_path):
        raise ValueError(
            f"Invalid file path: '{file_path}'. "
            "Only alphanumeric characters, underscores, hyphens, dots, and forward slashes are allowed."
        )

    return bucket_name, file_path
