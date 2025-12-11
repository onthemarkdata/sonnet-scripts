"""Init command implementation for sonnet-cli."""

from pathlib import Path
from typing import Dict, List, Optional, Any

from sonnet_cli.checks import check_docker_running, check_images_exist, detect_port_conflicts
from sonnet_cli.exceptions import DockerNotRunningError, ProjectExistsError
from sonnet_cli.services import DEFAULT_SERVICES, SERVICE_REGISTRY
from sonnet_cli.templates import (
    render_docker_compose,
    render_env_file,
    render_readme,
    render_init_sql,
    render_pgadmin_servers_json,
    render_pgadmin_preferences_json,
    render_pgadmin_pgpass,
)


def create_project(
    name: str,
    target_dir: Path,
    services: Optional[List[str]] = None,
    interactive: bool = False,
) -> Dict[str, Any]:
    """Create a new sonnet project.

    Args:
        name: Project name (will be used as directory name).
        target_dir: Parent directory where project will be created.
        services: List of services to include. If None, uses DEFAULT_SERVICES.
        interactive: Whether to prompt user for service selection.

    Returns:
        Dictionary with creation results including any warnings.

    Raises:
        DockerNotRunningError: If Docker daemon is not running.
        ProjectExistsError: If project directory already exists.
    """
    result: Dict[str, Any] = {
        "project_path": None,
        "services": [],
        "missing_images": [],
        "port_conflicts": {},
        "files_created": [],
    }

    # Check Docker is running
    if not check_docker_running():
        raise DockerNotRunningError()

    # Use default services if none specified
    if services is None:
        services = DEFAULT_SERVICES.copy()

    result["services"] = services

    # Check if project directory already exists
    project_path = target_dir / name
    if project_path.exists():
        raise ProjectExistsError(str(project_path))

    # Check for missing images
    available, missing = check_images_exist(services)
    result["missing_images"] = missing

    # Check for port conflicts
    conflicts = detect_port_conflicts(services)
    result["port_conflicts"] = conflicts

    # Create project directory structure
    project_path.mkdir(parents=True)
    result["project_path"] = project_path

    # Create config directories
    config_dir = project_path / "config"
    sql_dir = project_path / "sql"

    # Create docker-compose.yml
    compose_content = render_docker_compose(services, {"project_name": name})
    compose_file = project_path / "docker-compose.yml"
    compose_file.write_text(compose_content)
    result["files_created"].append(str(compose_file))

    # Create .env file
    env_content = render_env_file(services, {"project_name": name})
    env_file = project_path / ".env"
    env_file.write_text(env_content)
    result["files_created"].append(str(env_file))

    # Create README.md
    readme_content = render_readme(services, name)
    readme_file = project_path / "README.md"
    readme_file.write_text(readme_content)
    result["files_created"].append(str(readme_file))

    # Create sql directory and init.sql
    sql_dir.mkdir(parents=True, exist_ok=True)
    init_sql_content = render_init_sql(name)
    init_sql_file = sql_dir / "init.sql"
    init_sql_file.write_text(init_sql_content)
    result["files_created"].append(str(init_sql_file))

    # Create pgadmin config if pgadmin is selected
    if "pgadmin" in services:
        pgadmin_config_dir = config_dir / "pgadmin"
        pgadmin_config_dir.mkdir(parents=True, exist_ok=True)

        # servers.json
        servers_content = render_pgadmin_servers_json(name)
        servers_file = pgadmin_config_dir / "servers.json"
        servers_file.write_text(servers_content)
        result["files_created"].append(str(servers_file))

        # preferences.json
        prefs_content = render_pgadmin_preferences_json()
        prefs_file = pgadmin_config_dir / "preferences.json"
        prefs_file.write_text(prefs_content)
        result["files_created"].append(str(prefs_file))

        # pgpass
        pgpass_content = render_pgadmin_pgpass()
        pgpass_file = pgadmin_config_dir / "pgpass"
        pgpass_file.write_text(pgpass_content)
        result["files_created"].append(str(pgpass_file))

    return result
