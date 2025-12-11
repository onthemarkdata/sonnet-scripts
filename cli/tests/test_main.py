"""Tests for sonnet_cli.main module (CLI entry point)."""

import pytest
from typer.testing import CliRunner
from unittest.mock import patch, MagicMock

runner = CliRunner()


class TestCLICommands:
    """Tests for CLI command registration."""

    def test_cli_has_init_command(self):
        """CLI has an init command registered."""
        from sonnet_cli.main import app

        result = runner.invoke(app, ["--help"])
        assert "init" in result.output

    def test_cli_has_up_command(self):
        """CLI has an up command registered."""
        from sonnet_cli.main import app

        result = runner.invoke(app, ["--help"])
        assert "up" in result.output

    def test_cli_has_down_command(self):
        """CLI has a down command registered."""
        from sonnet_cli.main import app

        result = runner.invoke(app, ["--help"])
        assert "down" in result.output

    def test_cli_has_status_command(self):
        """CLI has a status command registered."""
        from sonnet_cli.main import app

        result = runner.invoke(app, ["--help"])
        assert "status" in result.output

    def test_cli_shows_help(self):
        """CLI shows help when invoked with --help."""
        from sonnet_cli.main import app

        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "init" in result.output
        assert "up" in result.output
        assert "down" in result.output
        assert "status" in result.output


class TestInitCommandCLI:
    """Tests for the init command via CLI."""

    def test_init_command_creates_project(self, tmp_path):
        """Init command creates a project when invoked."""
        from sonnet_cli.main import app

        with patch("sonnet_cli.main.check_docker_running", return_value=True):
            with patch("sonnet_cli.main.check_images_exist", return_value=(["pgduckdb", "pgadmin"], [])):
                with patch("sonnet_cli.main.detect_port_conflicts", return_value={}):
                    result = runner.invoke(
                        app,
                        ["init", "testproject", "--target-dir", str(tmp_path)],
                    )

        assert result.exit_code == 0
        assert (tmp_path / "testproject").exists()

    def test_init_command_shows_error_when_docker_not_running(self, tmp_path):
        """Init command shows error when Docker is not running."""
        from sonnet_cli.main import app

        with patch("sonnet_cli.main.check_docker_running", return_value=False):
            result = runner.invoke(
                app,
                ["init", "testproject", "--target-dir", str(tmp_path)],
            )

        assert result.exit_code != 0
        assert "Docker" in result.output or "docker" in result.output


class TestUpCommandCLI:
    """Tests for the up command via CLI."""

    def test_up_command_starts_services(self, tmp_path):
        """Up command starts services when invoked."""
        from sonnet_cli.main import app

        # Create a mock project
        compose_file = tmp_path / "docker-compose.yml"
        compose_file.write_text("services:\n  pgduckdb:\n    image: test")

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
            result = runner.invoke(app, ["up", "--project-dir", str(tmp_path)])

        assert result.exit_code == 0


class TestDownCommandCLI:
    """Tests for the down command via CLI."""

    def test_down_command_stops_services(self, tmp_path):
        """Down command stops services when invoked."""
        from sonnet_cli.main import app

        # Create a mock project
        compose_file = tmp_path / "docker-compose.yml"
        compose_file.write_text("services:\n  pgduckdb:\n    image: test")

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
            result = runner.invoke(app, ["down", "--project-dir", str(tmp_path)])

        assert result.exit_code == 0


class TestStatusCommandCLI:
    """Tests for the status command via CLI."""

    def test_status_command_shows_services(self, tmp_path):
        """Status command shows service status when invoked."""
        from sonnet_cli.main import app

        # Create a mock project
        compose_file = tmp_path / "docker-compose.yml"
        compose_file.write_text("services:\n  pgduckdb:\n    image: test")

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                returncode=0,
                stdout='[{"Name":"test_pgduckdb","State":"running","Ports":"5432"}]',
                stderr="",
            )
            result = runner.invoke(app, ["status", "--project-dir", str(tmp_path)])

        assert result.exit_code == 0
