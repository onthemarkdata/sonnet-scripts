"""Validation and pre-flight checks for sonnet-cli."""

import socket
import subprocess
from typing import List, Tuple, Dict

from sonnet_cli.services import SERVICE_REGISTRY


def check_docker_running() -> bool:
    """Check if Docker daemon is running.

    Returns:
        True if Docker is available and running, False otherwise.
    """
    try:
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True,
            timeout=10,
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def get_local_images() -> set:
    """Get set of locally available Docker images.

    Returns:
        Set of image names/tags available locally.
    """
    result = subprocess.run(
        ["docker", "images", "--format", "{{.Repository}}:{{.Tag}}"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return set()

    images = set()
    for line in result.stdout.strip().split("\n"):
        if line:
            images.add(line)
            # Also add just the repository name (without tag) for local images
            if ":" in line:
                images.add(line.split(":")[0])
    return images


def check_images_exist(services: List[str]) -> Tuple[List[str], List[str]]:
    """Check if required images exist for the given services.

    Pre-built images (from Docker Hub) are always considered available
    since they will be pulled automatically. Local images must be built
    from the sonnet-scripts repository.

    Args:
        services: List of service names to check.

    Returns:
        Tuple of (available_services, missing_services).
    """
    local_images = get_local_images()
    available = []
    missing = []

    for service in services:
        config = SERVICE_REGISTRY.get(service)
        if not config:
            continue

        image = config["image"]
        image_type = config.get("image_type", "prebuilt")

        if image_type == "local":
            # Local images must be built from sonnet-scripts repo
            if image in local_images:
                available.append(service)
            else:
                missing.append(service)
        else:
            # Pre-built images will be pulled automatically
            available.append(service)

    return available, missing


def check_port_available(port: int, host: str = "127.0.0.1") -> bool:
    """Check if a port is available for binding.

    Args:
        port: Port number to check.
        host: Host address to check (default: 127.0.0.1).

    Returns:
        True if port is available, False if in use.
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.settimeout(1)
        sock.bind((host, port))
        sock.close()
        return True
    except (socket.error, OSError):
        return False


def detect_port_conflicts(services: List[str]) -> Dict[str, List[int]]:
    """Detect port conflicts for selected services.

    Args:
        services: List of service names to check.

    Returns:
        Dictionary mapping service name to list of conflicting ports.
        Empty dict if no conflicts.
    """
    conflicts = {}

    for service in services:
        config = SERVICE_REGISTRY.get(service)
        if not config or not config.get("ports"):
            continue

        service_conflicts = []
        for host_port in config["ports"].keys():
            port = int(host_port)
            if not check_port_available(port):
                service_conflicts.append(port)

        if service_conflicts:
            conflicts[service] = service_conflicts

    return conflicts


def get_image_build_instructions(missing_services: List[str]) -> str:
    """Generate instructions for building missing images.

    Args:
        missing_services: List of service names with missing images.

    Returns:
        Formatted instruction string, or empty string if no missing images.
    """
    if not missing_services:
        return ""

    lines = [
        "",
        "The following services require locally-built images that were not found:",
    ]
    for service in missing_services:
        config = SERVICE_REGISTRY.get(service, {})
        image = config.get("image", service)
        lines.append(f"  - {service} (image: {image})")

    lines.extend(
        [
            "",
            "To build these images, run the following in the sonnet-scripts repository:",
            "",
            "    cd /path/to/sonnet-scripts",
            "    make setup",
            "",
            "This will build all required base images (linuxbase -> pythonbase -> services).",
        ]
    )
    return "\n".join(lines)


def format_port_conflict_message(conflicts: Dict[str, List[int]]) -> str:
    """Format port conflicts into a user-friendly message.

    Args:
        conflicts: Dictionary mapping service name to conflicting ports.

    Returns:
        Formatted message string.
    """
    if not conflicts:
        return ""

    lines = ["Port conflicts detected:", ""]
    for service, ports in conflicts.items():
        for port in ports:
            lines.append(f"  - Port {port} ({service}) is already in use")

    lines.extend(
        [
            "",
            "To resolve:",
            "  1. Stop the application using these ports, OR",
            "  2. Edit the generated docker-compose.yml to use different ports",
        ]
    )
    return "\n".join(lines)
