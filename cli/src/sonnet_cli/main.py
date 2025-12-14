"""Main CLI entry point for sonnet-cli."""

from pathlib import Path
from typing import Optional, List

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from sonnet_cli import __version__
from sonnet_cli.checks import (
    check_docker_running,
    check_images_exist,
    detect_port_conflicts,
    get_image_build_instructions,
    format_port_conflict_message,
)
from sonnet_cli.exceptions import (
    SonnetError,
    DockerNotRunningError,
    ProjectExistsError,
    NotASonnetProjectError,
)
from sonnet_cli.init_cmd import create_project
from sonnet_cli.services import DEFAULT_SERVICES, ALL_SERVICES, SERVICE_REGISTRY
from sonnet_cli.stack import up as stack_up, down as stack_down, status as stack_status

app = typer.Typer(
    name="sonnet",
    help="Create and manage local Modern Data Stack environments.",
    add_completion=False,
)
console = Console()


def version_callback(value: bool):
    """Print version and exit."""
    if value:
        console.print(f"sonnet-cli version {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        None,
        "--version",
        "-v",
        callback=version_callback,
        is_eager=True,
        help="Show version and exit.",
    ),
):
    """Sonnet CLI - Create and manage local Modern Data Stack environments."""
    pass


@app.command()
def init(
    name: str = typer.Argument(
        "sonnet-project",
        help="Name of the project to create.",
    ),
    target_dir: Path = typer.Option(
        Path.cwd(),
        "--target-dir",
        "-d",
        help="Directory where project will be created.",
    ),
    interactive: bool = typer.Option(
        False,
        "--interactive",
        "-i",
        help="Interactively select services to include.",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        help="Show verbose output.",
    ),
):
    """Create a new sonnet project with Docker Compose configuration."""
    try:
        # Check Docker first
        if not check_docker_running():
            raise DockerNotRunningError()

        # Determine services
        if interactive:
            services = _select_services_interactive()
        else:
            services = DEFAULT_SERVICES.copy()

        # Check for missing images
        available, missing = check_images_exist(services)
        if missing:
            console.print(
                Panel(
                    get_image_build_instructions(missing),
                    title="[yellow]Warning: Missing Images[/yellow]",
                    border_style="yellow",
                )
            )

        # Check for port conflicts
        conflicts = detect_port_conflicts(services)
        if conflicts:
            console.print(
                Panel(
                    format_port_conflict_message(conflicts),
                    title="[yellow]Warning: Port Conflicts[/yellow]",
                    border_style="yellow",
                )
            )

        # Create the project
        result = create_project(
            name=name,
            target_dir=target_dir,
            services=services,
            interactive=interactive,
        )

        # Success message
        console.print(f"\n[green]Success![/green] Created project '{name}'")
        console.print(f"\nNext steps:")
        console.print(f"  cd {name}")
        console.print(f"  sonnet up")

        # Show access info
        _print_access_info(services)

    except DockerNotRunningError:
        console.print(
            Panel(
                "Docker is not running.\n\nPlease start Docker Desktop or the Docker daemon and try again.",
                title="[red]Error[/red]",
                border_style="red",
            )
        )
        raise typer.Exit(1)
    except ProjectExistsError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)
    except SonnetError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


@app.command()
def up(
    project_dir: Path = typer.Option(
        Path.cwd(),
        "--project-dir",
        "-d",
        help="Project directory containing docker-compose.yml.",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        help="Show verbose output.",
    ),
):
    """Start all services in the project."""
    try:
        console.print("Starting services...")
        result = stack_up(project_dir)

        if result.get("missing_images"):
            console.print(
                Panel(
                    get_image_build_instructions(result["missing_images"]),
                    title="[yellow]Warning: Missing Images[/yellow]",
                    border_style="yellow",
                )
            )

        console.print("[green]All services started![/green]")

        # Show connection info
        _print_connection_info()

    except NotASonnetProjectError:
        console.print(
            "[red]Error:[/red] Not a sonnet project. No docker-compose.yml found."
        )
        console.print("Run 'sonnet init' to create a new project.")
        raise typer.Exit(1)
    except SonnetError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


@app.command()
def down(
    project_dir: Path = typer.Option(
        Path.cwd(),
        "--project-dir",
        "-d",
        help="Project directory containing docker-compose.yml.",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        help="Show verbose output.",
    ),
):
    """Stop all services in the project."""
    try:
        console.print("Stopping services...")
        result = stack_down(project_dir)
        console.print("[green]All services stopped.[/green]")
        console.print("\nNote: Your data is preserved in Docker volumes.")
        console.print("To remove volumes: docker compose down -v")

    except NotASonnetProjectError:
        console.print(
            "[red]Error:[/red] Not a sonnet project. No docker-compose.yml found."
        )
        raise typer.Exit(1)
    except SonnetError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


@app.command()
def status(
    project_dir: Path = typer.Option(
        Path.cwd(),
        "--project-dir",
        "-d",
        help="Project directory containing docker-compose.yml.",
    ),
):
    """Show status of all services in the project."""
    try:
        result = stack_status(project_dir)

        # Create status table
        table = Table(title="Service Status")
        table.add_column("Service", style="cyan")
        table.add_column("Status")
        table.add_column("Ports")

        for svc in result.get("services", []):
            state = svc.get("state", "unknown")
            state_style = "green" if state == "running" else "red"
            table.add_row(
                svc.get("name", ""),
                f"[{state_style}]{state}[/{state_style}]",
                svc.get("ports", ""),
            )

        console.print(table)

        # Show connection info if services are running
        if any(s.get("state") == "running" for s in result.get("services", [])):
            _print_connection_info()

    except NotASonnetProjectError:
        console.print(
            "[red]Error:[/red] Not a sonnet project. No docker-compose.yml found."
        )
        raise typer.Exit(1)
    except SonnetError as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)


def _select_services_interactive() -> List[str]:
    """Interactively select services to include.

    Returns:
        List of selected service names.
    """
    from rich.prompt import Prompt

    console.print("\n[bold]Select services for your stack:[/bold]\n")

    # pgduckdb is always included
    selected = ["pgduckdb"]
    console.print("[green]pgduckdb[/green] - PostgreSQL with DuckDB (always included)")

    # Let user select optional services
    optional = [s for s in ALL_SERVICES if s != "pgduckdb"]

    for service in optional:
        config = SERVICE_REGISTRY.get(service, {})
        desc = config.get("description", "")
        ports = config.get("ports", {})
        port_str = f" (port {list(ports.keys())[0]})" if ports else ""

        response = Prompt.ask(
            f"Include [cyan]{service}[/cyan] - {desc}{port_str}?",
            choices=["y", "n"],
            default="n" if service not in DEFAULT_SERVICES else "y",
        )
        if response == "y":
            selected.append(service)

    return selected


def _print_access_info(services: List[str]) -> None:
    """Print access information for selected services."""
    console.print("\n[bold]Access your stack:[/bold]")
    for service in services:
        config = SERVICE_REGISTRY.get(service, {})
        if "connection_string" in config:
            console.print(f"  {service}: {config['connection_string']}")
        elif "url_template" in config:
            console.print(f"  {service}: {config['url_template']}")


def _print_connection_info() -> None:
    """Print connection information for known services."""
    console.print("\n[bold]Connection Info:[/bold]")
    console.print("  Database: postgresql://postgres:postgres@localhost:5432/postgres")
    console.print("  pgAdmin:  http://localhost:8080 (pgadmin4@pgadmin.org / password)")


if __name__ == "__main__":
    app()
