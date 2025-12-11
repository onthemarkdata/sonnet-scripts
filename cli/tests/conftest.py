"""Shared pytest fixtures for sonnet-cli tests."""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock


@pytest.fixture
def temp_project_dir(tmp_path):
    """Create a temporary project directory."""
    project_dir = tmp_path / "test_project"
    project_dir.mkdir()
    return project_dir


@pytest.fixture
def mock_docker_available():
    """Mock Docker being available."""
    with patch("sonnet_cli.checks.check_docker_running", return_value=True):
        yield


@pytest.fixture
def mock_docker_unavailable():
    """Mock Docker being unavailable."""
    with patch("sonnet_cli.checks.check_docker_running", return_value=False):
        yield


@pytest.fixture
def mock_all_images_available():
    """Mock all images being available (including local builds)."""
    with patch("sonnet_cli.checks.get_local_images") as mock:
        mock.return_value = {
            "pgduckdb/pgduckdb:17-v0.1.0",
            "dpage/pgadmin4:9.3.0",
            "dbeaver/cloudbeaver:25.0.3",
            "minio/minio:RELEASE.2025-04-22T22-12-26Z",
            "jupyterbase",
            "pipelinebase",
            "dbtbase",
            "pythonbase",
            "linuxbase",
        }
        yield mock


@pytest.fixture
def mock_no_local_images():
    """Mock no local images built (only prebuilt available via pull)."""
    with patch("sonnet_cli.checks.get_local_images") as mock:
        mock.return_value = set()
        yield mock


@pytest.fixture
def mock_subprocess_success():
    """Mock subprocess.run returning success."""
    with patch("subprocess.run") as mock:
        mock.return_value = MagicMock(returncode=0, stdout="", stderr="")
        yield mock


@pytest.fixture
def mock_subprocess_failure():
    """Mock subprocess.run returning failure."""
    with patch("subprocess.run") as mock:
        mock.return_value = MagicMock(returncode=1, stdout="", stderr="Error")
        yield mock


@pytest.fixture
def sample_docker_compose_content():
    """Return sample docker-compose.yml content for testing."""
    return """services:
  pgduckdb:
    image: pgduckdb/pgduckdb:17-v0.1.0
    container_name: test_pgduckdb
    ports:
      - "5432:5432"
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: postgres
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "postgres"]
      retries: 5

  pgadmin:
    image: dpage/pgadmin4:9.3.0
    container_name: test_pgadmin
    ports:
      - "8080:80"
    depends_on:
      pgduckdb:
        condition: service_healthy

volumes:
  pgduckdb_data:
    driver: local
"""


@pytest.fixture
def sample_env_content():
    """Return sample .env content for testing."""
    return """# PostgreSQL Configuration
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=postgres
POSTGRES_HOST=pgduckdb
POSTGRES_PORT=5432
"""
