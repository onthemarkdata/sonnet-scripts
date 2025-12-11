"""Custom exceptions for sonnet-cli."""

from typing import Dict, List


class SonnetError(Exception):
    """Base exception for sonnet CLI."""

    pass


class DockerNotRunningError(SonnetError):
    """Docker daemon is not running."""

    def __init__(self):
        super().__init__(
            "Docker is not running. Please start Docker Desktop or the Docker daemon."
        )


class MissingImagesError(SonnetError):
    """Required Docker images are not available."""

    def __init__(self, missing: List[str], instructions: str):
        self.missing = missing
        self.instructions = instructions
        super().__init__(f"Missing images: {', '.join(missing)}")


class ProjectExistsError(SonnetError):
    """Project directory already exists."""

    def __init__(self, path: str):
        self.path = path
        super().__init__(f"Directory '{path}' already exists. Use --force to overwrite.")


class NotASonnetProjectError(SonnetError):
    """Current directory is not a sonnet project."""

    def __init__(self):
        super().__init__(
            "Not a sonnet project. No docker-compose.yml found.\n"
            "Run 'sonnet init' to create a new project."
        )


class PortConflictError(SonnetError):
    """Ports required by services are already in use."""

    def __init__(self, conflicts: Dict[str, List[int]]):
        self.conflicts = conflicts
        msg = self._format_message(conflicts)
        super().__init__(msg)

    @staticmethod
    def _format_message(conflicts: Dict[str, List[int]]) -> str:
        """Format port conflicts into a user-friendly message."""
        lines = ["Port conflicts detected:\n"]
        for service, ports in conflicts.items():
            for port in ports:
                lines.append(f"  - Port {port} ({service}) is already in use")
        lines.append("\nTo resolve:")
        lines.append("  1. Stop the application using these ports, OR")
        lines.append("  2. Edit the generated docker-compose.yml to use different ports")
        return "\n".join(lines)


class DockerComposeError(SonnetError):
    """Docker compose command failed."""

    def __init__(self, command: str, stderr: str):
        self.command = command
        self.stderr = stderr
        super().__init__(f"docker compose {command} failed:\n{stderr}")
