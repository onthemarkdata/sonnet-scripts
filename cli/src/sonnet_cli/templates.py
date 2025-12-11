"""Template rendering functions for sonnet-cli."""

from pathlib import Path
from typing import List, Dict, Any

from jinja2 import Environment, FileSystemLoader, select_autoescape

from sonnet_cli.services import SERVICE_REGISTRY, get_service_dependencies


def get_template_env() -> Environment:
    """Create and configure Jinja2 environment.

    Returns:
        Configured Jinja2 Environment instance.
    """
    template_dir = Path(__file__).parent / "templates"
    env = Environment(
        loader=FileSystemLoader(template_dir),
        autoescape=select_autoescape(["html", "xml"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    return env


def render_docker_compose(services: List[str], config: Dict[str, Any]) -> str:
    """Render docker-compose.yml template.

    Args:
        services: List of service names to include.
        config: Configuration dict with project_name and other settings.

    Returns:
        Rendered docker-compose.yml content.
    """
    env = get_template_env()
    template = env.get_template("docker-compose.yml.j2")

    # Get dependencies filtered to selected services
    dependencies = get_service_dependencies(services)

    return template.render(
        services=services,
        service_registry=SERVICE_REGISTRY,
        dependencies=dependencies,
        project_name=config.get("project_name", "sonnet-project"),
    )


def render_env_file(services: List[str], config: Dict[str, Any]) -> str:
    """Render .env template.

    Args:
        services: List of service names included in the project.
        config: Configuration dict with project_name and other settings.

    Returns:
        Rendered .env content.
    """
    env = get_template_env()
    template = env.get_template("env.j2")

    return template.render(
        services=services,
        project_name=config.get("project_name", "sonnet-project"),
    )


def render_readme(services: List[str], project_name: str) -> str:
    """Render README.md template.

    Args:
        services: List of service names included in the project.
        project_name: Name of the project.

    Returns:
        Rendered README.md content.
    """
    env = get_template_env()
    template = env.get_template("README.md.j2")

    return template.render(
        services=services,
        service_registry=SERVICE_REGISTRY,
        project_name=project_name,
    )


def render_init_sql(project_name: str) -> str:
    """Render init.sql template.

    Args:
        project_name: Name of the project.

    Returns:
        Rendered init.sql content.
    """
    env = get_template_env()
    template = env.get_template("init.sql.j2")

    return template.render(project_name=project_name)


def render_pgadmin_servers_json(project_name: str) -> str:
    """Render pgAdmin servers.json template.

    Args:
        project_name: Name of the project.

    Returns:
        Rendered servers.json content.
    """
    env = get_template_env()
    template = env.get_template("pgadmin/servers.json.j2")

    return template.render(project_name=project_name)


def render_pgadmin_preferences_json() -> str:
    """Render pgAdmin preferences.json template.

    Returns:
        Rendered preferences.json content.
    """
    env = get_template_env()
    template = env.get_template("pgadmin/preferences.json.j2")

    return template.render()


def render_pgadmin_pgpass() -> str:
    """Render pgAdmin pgpass template.

    Returns:
        Rendered pgpass content.
    """
    env = get_template_env()
    template = env.get_template("pgadmin/pgpass.j2")

    return template.render()
