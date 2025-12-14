"""Tests for sonnet_cli.stack module."""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock


class TestUpCommand:
    """Tests for the up command."""

    def test_up_calls_docker_compose_up(self, tmp_path):
        """Up command calls docker compose up -d."""
        from sonnet_cli.stack import up

        # Create a mock project directory with docker-compose.yml
        compose_file = tmp_path / "docker-compose.yml"
        compose_file.write_text("services:\n  pgduckdb:\n    image: test")

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
            result = up(project_dir=tmp_path)

        # Check that docker compose up was called (among other calls)
        compose_up_calls = [
            call for call in mock_run.call_args_list
            if "compose" in call[0][0] and "up" in call[0][0]
        ]
        assert len(compose_up_calls) == 1
        call_args = compose_up_calls[0]
        assert "docker" in call_args[0][0]
        assert "-d" in call_args[0][0]

    def test_up_fails_when_not_in_project_dir(self, tmp_path):
        """Up raises error when not in a sonnet project directory."""
        from sonnet_cli.stack import up
        from sonnet_cli.exceptions import NotASonnetProjectError

        # Empty directory - no docker-compose.yml
        with pytest.raises(NotASonnetProjectError):
            up(project_dir=tmp_path)

    def test_up_checks_images_before_starting(self, tmp_path):
        """Up checks for missing images before starting."""
        from sonnet_cli.stack import up

        # Create a mock project with docker-compose.yml
        compose_file = tmp_path / "docker-compose.yml"
        compose_file.write_text(
            """services:
  pgduckdb:
    image: pgduckdb/pgduckdb:17-v0.1.0
  jupyterbase:
    image: jupyterbase
"""
        )

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
            with patch(
                "sonnet_cli.stack.check_images_exist",
                return_value=(["pgduckdb"], ["jupyterbase"]),
            ) as mock_check:
                result = up(project_dir=tmp_path)

        # Should have checked images
        mock_check.assert_called_once()
        # Result should include missing images warning
        assert "jupyterbase" in result.get("missing_images", [])

    def test_up_returns_success_info(self, tmp_path):
        """Up returns success information with service details."""
        from sonnet_cli.stack import up

        compose_file = tmp_path / "docker-compose.yml"
        compose_file.write_text("services:\n  pgduckdb:\n    image: test")

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
            with patch("sonnet_cli.stack.check_images_exist", return_value=(["pgduckdb"], [])):
                result = up(project_dir=tmp_path)

        assert result.get("success") is True


class TestDownCommand:
    """Tests for the down command."""

    def test_down_calls_docker_compose_down(self, tmp_path):
        """Down command calls docker compose down."""
        from sonnet_cli.stack import down

        compose_file = tmp_path / "docker-compose.yml"
        compose_file.write_text("services:\n  pgduckdb:\n    image: test")

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0, stdout="", stderr="")
            result = down(project_dir=tmp_path)

        mock_run.assert_called_once()
        call_args = mock_run.call_args
        assert "docker" in call_args[0][0]
        assert "compose" in call_args[0][0]
        assert "down" in call_args[0][0]

    def test_down_fails_when_not_in_project_dir(self, tmp_path):
        """Down raises error when not in a sonnet project directory."""
        from sonnet_cli.stack import down
        from sonnet_cli.exceptions import NotASonnetProjectError

        with pytest.raises(NotASonnetProjectError):
            down(project_dir=tmp_path)


class TestStatusCommand:
    """Tests for the status command."""

    def test_status_shows_running_services(self, tmp_path):
        """Status shows information about running services."""
        from sonnet_cli.stack import status

        compose_file = tmp_path / "docker-compose.yml"
        compose_file.write_text("services:\n  pgduckdb:\n    image: test\n    ports:\n      - '5432:5432'")

        with patch("subprocess.run") as mock_run:
            # Mock docker compose ps output
            mock_run.return_value = MagicMock(
                returncode=0,
                stdout='[{"Name":"test_pgduckdb","State":"running","Ports":"0.0.0.0:5432->5432/tcp"}]',
                stderr="",
            )
            result = status(project_dir=tmp_path)

        assert "services" in result
        assert len(result["services"]) > 0

    def test_status_shows_stopped_services(self, tmp_path):
        """Status shows stopped services correctly."""
        from sonnet_cli.stack import status

        compose_file = tmp_path / "docker-compose.yml"
        compose_file.write_text("services:\n  pgduckdb:\n    image: test")

        with patch("subprocess.run") as mock_run:
            # Mock docker compose ps with stopped services
            mock_run.return_value = MagicMock(
                returncode=0,
                stdout='[{"Name":"test_pgduckdb","State":"exited","Ports":""}]',
                stderr="",
            )
            result = status(project_dir=tmp_path)

        assert "services" in result
        # Should show the service even if stopped
        assert any(s.get("state") == "exited" for s in result["services"])

    def test_status_displays_connection_strings(self, tmp_path):
        """Status includes connection strings for database services."""
        from sonnet_cli.stack import status

        compose_file = tmp_path / "docker-compose.yml"
        compose_file.write_text("services:\n  pgduckdb:\n    image: pgduckdb/pgduckdb:17-v0.1.0\n    ports:\n      - '5432:5432'")

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                returncode=0,
                stdout='[{"Name":"test_pgduckdb","State":"running","Ports":"0.0.0.0:5432->5432/tcp"}]',
                stderr="",
            )
            result = status(project_dir=tmp_path)

        # Should include connection info
        assert "connection_info" in result

    def test_status_fails_when_not_in_project_dir(self, tmp_path):
        """Status raises error when not in a sonnet project directory."""
        from sonnet_cli.stack import status
        from sonnet_cli.exceptions import NotASonnetProjectError

        with pytest.raises(NotASonnetProjectError):
            status(project_dir=tmp_path)
