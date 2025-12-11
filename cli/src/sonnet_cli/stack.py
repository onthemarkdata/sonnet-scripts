"""Stack lifecycle commands (up, down, status) for sonnet-cli."""

import json
import subprocess
from pathlib import Path
from typing import Dict, Any, List

from sonnet_cli.checks import check_images_exist
from sonnet_cli.exceptions import NotASonnetProjectError, DockerComposeError
from sonnet_cli.services import SERVICE_REGISTRY


def _validate_project_dir(project_dir: Path) -> None:
    """Validate that the directory is a sonnet project.

    Args:
        project_dir: Path to the project directory.

    Raises:
        NotASonnetProjectError: If docker-compose.yml doesn't exist.
    """
    compose_file = project_dir / "docker-compose.yml"
    if not compose_file.exists():
        raise NotASonnetProjectError()


def _parse_services_from_compose(project_dir: Path) -> List[str]:
    """Parse service names from docker-compose.yml.

    Args:
        project_dir: Path to the project directory.

    Returns:
        List of service names defined in the compose file.
    """
    import yaml

    compose_file = project_dir / "docker-compose.yml"
    try:
        with open(compose_file) as f:
            compose = yaml.safe_load(f)
        return list(compose.get("services", {}).keys())
    except Exception:
        return []


def up(project_dir: Path) -> Dict[str, Any]:
    """Start all services in the project.

    Args:
        project_dir: Path to the project directory.

    Returns:
        Dictionary with operation results.

    Raises:
        NotASonnetProjectError: If not a valid sonnet project.
        DockerComposeError: If docker compose command fails.
    """
    _validate_project_dir(project_dir)

    result: Dict[str, Any] = {
        "success": False,
        "missing_images": [],
        "services_started": [],
    }

    # Get services from compose file and check images
    services = _parse_services_from_compose(project_dir)
    available, missing = check_images_exist(services)
    result["missing_images"] = missing

    # Run docker compose up
    cmd = ["docker", "compose", "up", "-d"]
    proc = subprocess.run(
        cmd,
        cwd=project_dir,
        capture_output=True,
        text=True,
    )

    if proc.returncode != 0:
        raise DockerComposeError("up", proc.stderr)

    result["success"] = True
    result["services_started"] = services
    return result


def down(project_dir: Path) -> Dict[str, Any]:
    """Stop all services in the project.

    Args:
        project_dir: Path to the project directory.

    Returns:
        Dictionary with operation results.

    Raises:
        NotASonnetProjectError: If not a valid sonnet project.
        DockerComposeError: If docker compose command fails.
    """
    _validate_project_dir(project_dir)

    result: Dict[str, Any] = {
        "success": False,
        "services_stopped": [],
    }

    # Get services before stopping
    services = _parse_services_from_compose(project_dir)

    # Run docker compose down
    cmd = ["docker", "compose", "down"]
    proc = subprocess.run(
        cmd,
        cwd=project_dir,
        capture_output=True,
        text=True,
    )

    if proc.returncode != 0:
        raise DockerComposeError("down", proc.stderr)

    result["success"] = True
    result["services_stopped"] = services
    return result


def status(project_dir: Path) -> Dict[str, Any]:
    """Get status of all services in the project.

    Args:
        project_dir: Path to the project directory.

    Returns:
        Dictionary with service status information.

    Raises:
        NotASonnetProjectError: If not a valid sonnet project.
    """
    _validate_project_dir(project_dir)

    result: Dict[str, Any] = {
        "services": [],
        "connection_info": {},
    }

    # Run docker compose ps --format json
    cmd = ["docker", "compose", "ps", "--format", "json"]
    proc = subprocess.run(
        cmd,
        cwd=project_dir,
        capture_output=True,
        text=True,
    )

    if proc.returncode == 0 and proc.stdout.strip():
        try:
            # Parse JSON output (could be array or newline-separated objects)
            stdout = proc.stdout.strip()
            if stdout.startswith("["):
                services_data = json.loads(stdout)
            else:
                # Newline-separated JSON objects
                services_data = [json.loads(line) for line in stdout.split("\n") if line]

            for svc in services_data:
                service_info = {
                    "name": svc.get("Name", ""),
                    "state": svc.get("State", "unknown"),
                    "ports": svc.get("Ports", ""),
                }
                result["services"].append(service_info)
        except json.JSONDecodeError:
            pass

    # Add connection info for known services
    result["connection_info"] = _get_connection_info()

    return result


def _get_connection_info() -> Dict[str, str]:
    """Get connection information for known services.

    Returns:
        Dictionary mapping service names to connection strings/URLs.
    """
    info = {}
    for name, config in SERVICE_REGISTRY.items():
        if "connection_string" in config:
            info[name] = config["connection_string"]
        elif "url_template" in config:
            info[name] = config["url_template"]
    return info
