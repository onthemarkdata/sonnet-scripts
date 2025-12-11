"""Service registry containing configuration for all available services."""

from typing import Any, Dict, List, Tuple


SERVICE_REGISTRY: Dict[str, Dict[str, Any]] = {
    "pgduckdb": {
        "image": "pgduckdb/pgduckdb:17-v0.1.0",
        "image_type": "prebuilt",
        "ports": {"5432": 5432},
        "required": True,
        "environment": {
            "POSTGRES_USER": "postgres",
            "POSTGRES_PASSWORD": "postgres",
            "POSTGRES_DB": "postgres",
        },
        "volumes": ["pgduckdb_data:/var/lib/postgresql/data"],
        "healthcheck": {
            "test": ["CMD", "pg_isready", "-U", "postgres"],
            "retries": 5,
        },
        "description": "PostgreSQL with DuckDB extension",
        "connection_string": "postgresql://postgres:postgres@localhost:5432/postgres",
    },
    "pgadmin": {
        "image": "dpage/pgadmin4:9.3.0",
        "image_type": "prebuilt",
        "ports": {"8080": 80},
        "required": False,
        "depends_on": ["pgduckdb"],
        "requires_config_files": True,
        "environment": {
            "PGADMIN_DEFAULT_EMAIL": "pgadmin4@pgadmin.org",
            "PGADMIN_DEFAULT_PASSWORD": "password",
            "PGADMIN_CONFIG_SERVER_MODE": "False",
            "PGADMIN_CONFIG_MASTER_PASSWORD_REQUIRED": "False",
            "PGADMIN_PREFERENCES_JSON_FILE": "/pgadmin4/preferences.json",
            "PGADMIN_CONFIG_CONSOLE_LOG_LEVEL": "10",
        },
        "description": "pgAdmin 4 web interface",
        "url_template": "http://localhost:8080",
    },
    "cloudbeaver": {
        "image": "dbeaver/cloudbeaver:25.0.3",
        "image_type": "prebuilt",
        "ports": {"8978": 8978},
        "required": False,
        "depends_on": ["pgduckdb"],
        "volumes": ["cloudbeaver-data:/opt/cloudbeaver/workspace"],
        "description": "CloudBeaver web interface",
        "url_template": "http://localhost:8978",
    },
    "minio": {
        "image": "minio/minio:RELEASE.2025-04-22T22-12-26Z",
        "image_type": "prebuilt",
        "ports": {"9000": 9000, "9001": 9001},
        "required": False,
        "environment": {
            "MINIO_ROOT_USER": "admin",
            "MINIO_ROOT_PASSWORD": "password",
            "MINIO_DOMAIN": "minio",
        },
        "command": ["server", "/data", "--console-address", ":9001"],
        "description": "S3-compatible object storage",
        "url_template": "http://localhost:9001",
    },
    "jupyterbase": {
        "image": "jupyterbase",
        "image_type": "local",
        "ports": {"8888": 8888},
        "required": False,
        "depends_on": ["pgduckdb"],
        "description": "Jupyter Lab for Python/SQL",
        "url_template": "http://localhost:8888",
    },
    "pipelinebase": {
        "image": "pipelinebase",
        "image_type": "local",
        "ports": {},
        "required": False,
        "depends_on": ["pgduckdb", "minio"],
        "description": "ETL pipelines and data loading",
    },
    "dbtbase": {
        "image": "dbtbase",
        "image_type": "local",
        "ports": {},
        "required": False,
        "depends_on": ["pgduckdb"],
        "environment": {
            "DB_HOST": "pgduckdb",
            "DB_USER": "postgres",
            "DB_PASSWORD": "postgres",
            "DB_NAME": "postgres",
            "DBT_TARGET": "dev",
        },
        "volumes": ["dbt_data:/apps/data"],
        "description": "dbt Core for transformations",
    },
}

# Default services for non-interactive init
DEFAULT_SERVICES: List[str] = ["pgduckdb", "pgadmin"]

# All available services for interactive selection
ALL_SERVICES: List[str] = list(SERVICE_REGISTRY.keys())

# Services that require local builds (from sonnet-scripts repo)
LOCAL_BUILD_SERVICES: List[str] = [
    name for name, config in SERVICE_REGISTRY.items() if config["image_type"] == "local"
]

# Services with pre-built images (pulled from Docker Hub)
PREBUILT_SERVICES: List[str] = [
    name for name, config in SERVICE_REGISTRY.items() if config["image_type"] == "prebuilt"
]


def get_service_ports(services: List[str]) -> Dict[str, List[int]]:
    """Get all ports used by the given services.

    Args:
        services: List of service names

    Returns:
        Dictionary mapping service name to list of host ports
    """
    result: Dict[str, List[int]] = {}
    for service in services:
        if service in SERVICE_REGISTRY:
            ports = SERVICE_REGISTRY[service].get("ports", {})
            if ports:
                result[service] = [int(p) for p in ports.keys()]
    return result


def get_required_images(services: List[str]) -> Tuple[List[str], List[str]]:
    """Get required images for the given services, split by type.

    Args:
        services: List of service names

    Returns:
        Tuple of (prebuilt_images, local_images)
    """
    prebuilt: List[str] = []
    local: List[str] = []
    for service in services:
        if service in SERVICE_REGISTRY:
            config = SERVICE_REGISTRY[service]
            if config["image_type"] == "local":
                local.append(config["image"])
            else:
                prebuilt.append(config["image"])
    return prebuilt, local


def get_service_dependencies(services: List[str]) -> Dict[str, List[str]]:
    """Get dependencies for the given services (filtered to selected services only).

    Args:
        services: List of service names

    Returns:
        Dictionary mapping service name to list of dependencies (within selected services)
    """
    result: Dict[str, List[str]] = {}
    for service in services:
        if service in SERVICE_REGISTRY:
            deps = SERVICE_REGISTRY[service].get("depends_on", [])
            # Only include dependencies that are in the selected services
            filtered_deps = [d for d in deps if d in services]
            if filtered_deps:
                result[service] = filtered_deps
    return result
