"""Tests for sonnet_cli.checks module."""

import pytest
from unittest.mock import patch, MagicMock
import socket


class TestCheckDockerRunning:
    """Tests for check_docker_running function."""

    def test_check_docker_running_returns_true_when_available(self):
        """Docker check returns True when docker info succeeds."""
        from sonnet_cli.checks import check_docker_running

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            assert check_docker_running() is True

    def test_check_docker_running_returns_false_when_unavailable(self):
        """Docker check returns False when docker info fails."""
        from sonnet_cli.checks import check_docker_running

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=1)
            assert check_docker_running() is False

    def test_check_docker_running_returns_false_on_timeout(self):
        """Docker check returns False when command times out."""
        from sonnet_cli.checks import check_docker_running
        import subprocess

        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.TimeoutExpired(cmd="docker", timeout=10)
            assert check_docker_running() is False

    def test_check_docker_running_returns_false_when_docker_not_installed(self):
        """Docker check returns False when docker command not found."""
        from sonnet_cli.checks import check_docker_running

        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = FileNotFoundError()
            assert check_docker_running() is False


class TestGetLocalImages:
    """Tests for get_local_images function."""

    def test_get_local_images_returns_set_of_images(self):
        """Returns set of locally available docker images."""
        from sonnet_cli.checks import get_local_images

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(
                returncode=0,
                stdout="pythonbase:latest\npipelinebase:latest\npgduckdb/pgduckdb:17-v0.1.0\n",
            )
            images = get_local_images()
            assert "pythonbase:latest" in images
            assert "pythonbase" in images  # Should also have just the repo name
            assert "pipelinebase:latest" in images
            assert "pgduckdb/pgduckdb:17-v0.1.0" in images

    def test_get_local_images_returns_empty_set_on_failure(self):
        """Returns empty set when docker images command fails."""
        from sonnet_cli.checks import get_local_images

        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=1, stdout="")
            images = get_local_images()
            assert images == set()


class TestCheckImagesExist:
    """Tests for check_images_exist function."""

    def test_check_images_exist_prebuilt_always_available(self):
        """Pre-built images are always considered available."""
        from sonnet_cli.checks import check_images_exist

        with patch("sonnet_cli.checks.get_local_images", return_value=set()):
            available, missing = check_images_exist(["pgduckdb", "pgadmin"])
            assert "pgduckdb" in available
            assert "pgadmin" in available
            assert missing == []

    def test_check_images_exist_local_missing_when_not_built(self):
        """Local images are missing when not in local docker images."""
        from sonnet_cli.checks import check_images_exist

        with patch("sonnet_cli.checks.get_local_images", return_value=set()):
            available, missing = check_images_exist(["jupyterbase", "pipelinebase"])
            assert "jupyterbase" in missing
            assert "pipelinebase" in missing
            assert available == []

    def test_check_images_exist_local_available_when_built(self):
        """Local images are available when present in local docker images."""
        from sonnet_cli.checks import check_images_exist

        with patch(
            "sonnet_cli.checks.get_local_images",
            return_value={"jupyterbase", "pipelinebase", "dbtbase"},
        ):
            available, missing = check_images_exist(["jupyterbase", "pipelinebase"])
            assert "jupyterbase" in available
            assert "pipelinebase" in available
            assert missing == []

    def test_check_images_exist_mixed_services(self):
        """Correctly handles mix of prebuilt and local services."""
        from sonnet_cli.checks import check_images_exist

        with patch("sonnet_cli.checks.get_local_images", return_value={"jupyterbase"}):
            available, missing = check_images_exist(
                ["pgduckdb", "pgadmin", "jupyterbase", "pipelinebase"]
            )
            assert "pgduckdb" in available
            assert "pgadmin" in available
            assert "jupyterbase" in available
            assert "pipelinebase" in missing


class TestCheckPortAvailable:
    """Tests for check_port_available function."""

    def test_check_port_available_returns_true_for_free_port(self):
        """Returns True when port is available."""
        from sonnet_cli.checks import check_port_available

        # Use a high port that's unlikely to be in use
        assert check_port_available(59999) is True

    def test_check_port_available_returns_false_for_used_port(self):
        """Returns False when port is in use."""
        from sonnet_cli.checks import check_port_available

        # Create a socket to occupy the port
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            sock.bind(("127.0.0.1", 59998))
            sock.listen(1)
            assert check_port_available(59998) is False
        finally:
            sock.close()


class TestDetectPortConflicts:
    """Tests for detect_port_conflicts function."""

    def test_detect_port_conflicts_empty_when_no_conflicts(self):
        """Returns empty dict when all ports are available."""
        from sonnet_cli.checks import detect_port_conflicts

        with patch("sonnet_cli.checks.check_port_available", return_value=True):
            conflicts = detect_port_conflicts(["pgduckdb", "pgadmin"])
            assert conflicts == {}

    def test_detect_port_conflicts_returns_conflicting_ports(self):
        """Returns dict with conflicting ports."""
        from sonnet_cli.checks import detect_port_conflicts

        def mock_port_check(port, host="127.0.0.1"):
            # Simulate port 5432 being in use
            return port != 5432

        with patch("sonnet_cli.checks.check_port_available", side_effect=mock_port_check):
            conflicts = detect_port_conflicts(["pgduckdb", "pgadmin"])
            assert "pgduckdb" in conflicts
            assert 5432 in conflicts["pgduckdb"]
            assert "pgadmin" not in conflicts

    def test_detect_port_conflicts_handles_services_without_ports(self):
        """Services without exposed ports don't cause conflicts."""
        from sonnet_cli.checks import detect_port_conflicts

        with patch("sonnet_cli.checks.check_port_available", return_value=True):
            # pipelinebase has no exposed ports
            conflicts = detect_port_conflicts(["pipelinebase", "dbtbase"])
            assert conflicts == {}


class TestGetImageBuildInstructions:
    """Tests for get_image_build_instructions function."""

    def test_get_image_build_instructions_formats_correctly(self):
        """Instructions include missing images and build command."""
        from sonnet_cli.checks import get_image_build_instructions

        instructions = get_image_build_instructions(["jupyterbase", "pipelinebase"])
        assert "jupyterbase" in instructions
        assert "pipelinebase" in instructions
        assert "make setup" in instructions
        assert "sonnet-scripts" in instructions

    def test_get_image_build_instructions_returns_empty_for_no_missing(self):
        """Returns empty string when no images are missing."""
        from sonnet_cli.checks import get_image_build_instructions

        instructions = get_image_build_instructions([])
        assert instructions == ""
