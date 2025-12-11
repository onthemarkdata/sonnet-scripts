"""Tests for sonnet_cli.init_cmd module."""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from typer.testing import CliRunner


runner = CliRunner()


class TestInitCommand:
    """Tests for the init command."""

    def test_init_creates_project_directory(self, tmp_path):
        """Init creates the project directory."""
        from sonnet_cli.init_cmd import create_project

        project_path = tmp_path / "myproject"

        with patch("sonnet_cli.init_cmd.check_docker_running", return_value=True):
            with patch("sonnet_cli.init_cmd.check_images_exist", return_value=(["pgduckdb", "pgadmin"], [])):
                with patch("sonnet_cli.init_cmd.detect_port_conflicts", return_value={}):
                    create_project(
                        name="myproject",
                        target_dir=tmp_path,
                        services=["pgduckdb", "pgadmin"],
                        interactive=False,
                    )

        assert project_path.exists()
        assert project_path.is_dir()

    def test_init_fails_if_directory_exists(self, tmp_path):
        """Init raises error if directory already exists."""
        from sonnet_cli.init_cmd import create_project
        from sonnet_cli.exceptions import ProjectExistsError

        # Create directory first
        project_path = tmp_path / "existing"
        project_path.mkdir()

        with pytest.raises(ProjectExistsError):
            create_project(
                name="existing",
                target_dir=tmp_path,
                services=["pgduckdb"],
                interactive=False,
            )

    def test_init_creates_docker_compose_yml(self, tmp_path):
        """Init creates docker-compose.yml file."""
        from sonnet_cli.init_cmd import create_project

        with patch("sonnet_cli.init_cmd.check_docker_running", return_value=True):
            with patch("sonnet_cli.init_cmd.check_images_exist", return_value=(["pgduckdb", "pgadmin"], [])):
                with patch("sonnet_cli.init_cmd.detect_port_conflicts", return_value={}):
                    create_project(
                        name="myproject",
                        target_dir=tmp_path,
                        services=["pgduckdb", "pgadmin"],
                        interactive=False,
                    )

        compose_file = tmp_path / "myproject" / "docker-compose.yml"
        assert compose_file.exists()
        content = compose_file.read_text()
        assert "pgduckdb" in content
        assert "pgadmin" in content

    def test_init_creates_env_file(self, tmp_path):
        """Init creates .env file."""
        from sonnet_cli.init_cmd import create_project

        with patch("sonnet_cli.init_cmd.check_docker_running", return_value=True):
            with patch("sonnet_cli.init_cmd.check_images_exist", return_value=(["pgduckdb"], [])):
                with patch("sonnet_cli.init_cmd.detect_port_conflicts", return_value={}):
                    create_project(
                        name="myproject",
                        target_dir=tmp_path,
                        services=["pgduckdb"],
                        interactive=False,
                    )

        env_file = tmp_path / "myproject" / ".env"
        assert env_file.exists()
        content = env_file.read_text()
        assert "POSTGRES_USER" in content

    def test_init_creates_readme(self, tmp_path):
        """Init creates README.md file."""
        from sonnet_cli.init_cmd import create_project

        with patch("sonnet_cli.init_cmd.check_docker_running", return_value=True):
            with patch("sonnet_cli.init_cmd.check_images_exist", return_value=(["pgduckdb"], [])):
                with patch("sonnet_cli.init_cmd.detect_port_conflicts", return_value={}):
                    create_project(
                        name="myproject",
                        target_dir=tmp_path,
                        services=["pgduckdb"],
                        interactive=False,
                    )

        readme_file = tmp_path / "myproject" / "README.md"
        assert readme_file.exists()
        content = readme_file.read_text()
        assert "myproject" in content

    def test_init_creates_pgadmin_config_when_selected(self, tmp_path):
        """Init creates pgadmin config files when pgadmin is selected."""
        from sonnet_cli.init_cmd import create_project

        with patch("sonnet_cli.init_cmd.check_docker_running", return_value=True):
            with patch("sonnet_cli.init_cmd.check_images_exist", return_value=(["pgduckdb", "pgadmin"], [])):
                with patch("sonnet_cli.init_cmd.detect_port_conflicts", return_value={}):
                    create_project(
                        name="myproject",
                        target_dir=tmp_path,
                        services=["pgduckdb", "pgadmin"],
                        interactive=False,
                    )

        servers_json = tmp_path / "myproject" / "config" / "pgadmin" / "servers.json"
        assert servers_json.exists()
        content = servers_json.read_text()
        assert "pgduckdb" in content

    def test_init_uses_default_services_when_not_interactive(self, tmp_path):
        """Init uses default services (pgduckdb, pgadmin) when not interactive."""
        from sonnet_cli.init_cmd import create_project
        from sonnet_cli.services import DEFAULT_SERVICES

        with patch("sonnet_cli.init_cmd.check_docker_running", return_value=True):
            with patch("sonnet_cli.init_cmd.check_images_exist", return_value=(DEFAULT_SERVICES, [])):
                with patch("sonnet_cli.init_cmd.detect_port_conflicts", return_value={}):
                    create_project(
                        name="myproject",
                        target_dir=tmp_path,
                        services=None,  # Should use defaults
                        interactive=False,
                    )

        compose_file = tmp_path / "myproject" / "docker-compose.yml"
        content = compose_file.read_text()
        # Default services are pgduckdb and pgadmin
        assert "pgduckdb" in content
        assert "pgadmin" in content

    def test_init_returns_warning_when_images_missing(self, tmp_path):
        """Init returns warning info when local images are missing."""
        from sonnet_cli.init_cmd import create_project

        with patch("sonnet_cli.init_cmd.check_docker_running", return_value=True):
            with patch(
                "sonnet_cli.init_cmd.check_images_exist",
                return_value=(["pgduckdb"], ["jupyterbase"]),
            ):
                with patch("sonnet_cli.init_cmd.detect_port_conflicts", return_value={}):
                    result = create_project(
                        name="myproject",
                        target_dir=tmp_path,
                        services=["pgduckdb", "jupyterbase"],
                        interactive=False,
                    )

        # Should return info about missing images
        assert result.get("missing_images") == ["jupyterbase"]

    def test_init_returns_warning_on_port_conflicts(self, tmp_path):
        """Init returns warning info when ports are in use."""
        from sonnet_cli.init_cmd import create_project

        with patch("sonnet_cli.init_cmd.check_docker_running", return_value=True):
            with patch("sonnet_cli.init_cmd.check_images_exist", return_value=(["pgduckdb", "pgadmin"], [])):
                with patch(
                    "sonnet_cli.init_cmd.detect_port_conflicts",
                    return_value={"pgduckdb": [5432]},
                ):
                    result = create_project(
                        name="myproject",
                        target_dir=tmp_path,
                        services=["pgduckdb", "pgadmin"],
                        interactive=False,
                    )

        # Should return info about port conflicts
        assert result.get("port_conflicts") == {"pgduckdb": [5432]}

    def test_init_creates_sql_directory(self, tmp_path):
        """Init creates sql directory with init.sql."""
        from sonnet_cli.init_cmd import create_project

        with patch("sonnet_cli.init_cmd.check_docker_running", return_value=True):
            with patch("sonnet_cli.init_cmd.check_images_exist", return_value=(["pgduckdb"], [])):
                with patch("sonnet_cli.init_cmd.detect_port_conflicts", return_value={}):
                    create_project(
                        name="myproject",
                        target_dir=tmp_path,
                        services=["pgduckdb"],
                        interactive=False,
                    )

        sql_file = tmp_path / "myproject" / "sql" / "init.sql"
        assert sql_file.exists()


class TestCheckDockerBeforeInit:
    """Tests for Docker availability checks before init."""

    def test_init_raises_error_when_docker_not_running(self, tmp_path):
        """Init raises error when Docker is not running."""
        from sonnet_cli.init_cmd import create_project
        from sonnet_cli.exceptions import DockerNotRunningError

        with patch("sonnet_cli.init_cmd.check_docker_running", return_value=False):
            with pytest.raises(DockerNotRunningError):
                create_project(
                    name="myproject",
                    target_dir=tmp_path,
                    services=["pgduckdb"],
                    interactive=False,
                )
