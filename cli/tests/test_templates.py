"""Tests for sonnet_cli.templates module."""

import pytest
import yaml


class TestRenderDockerCompose:
    """Tests for render_docker_compose function."""

    def test_render_docker_compose_includes_selected_services(self):
        """Generated compose includes all selected services."""
        from sonnet_cli.templates import render_docker_compose

        result = render_docker_compose(
            services=["pgduckdb", "pgadmin"],
            config={"project_name": "test_project"},
        )
        # Parse YAML to verify structure
        compose = yaml.safe_load(result)
        assert "pgduckdb" in compose["services"]
        assert "pgadmin" in compose["services"]

    def test_render_docker_compose_includes_pgduckdb_healthcheck(self):
        """pgduckdb service has healthcheck configured."""
        from sonnet_cli.templates import render_docker_compose

        result = render_docker_compose(
            services=["pgduckdb"],
            config={"project_name": "test_project"},
        )
        compose = yaml.safe_load(result)
        assert "healthcheck" in compose["services"]["pgduckdb"]
        assert compose["services"]["pgduckdb"]["healthcheck"]["retries"] == 5

    def test_render_docker_compose_sets_correct_ports(self):
        """Services have correct port mappings."""
        from sonnet_cli.templates import render_docker_compose

        result = render_docker_compose(
            services=["pgduckdb", "pgadmin"],
            config={"project_name": "test_project"},
        )
        compose = yaml.safe_load(result)
        # pgduckdb should have port 5432
        assert "5432:5432" in compose["services"]["pgduckdb"]["ports"]
        # pgadmin should have port 8080 -> 80
        assert "8080:80" in compose["services"]["pgadmin"]["ports"]

    def test_render_docker_compose_handles_dependencies(self):
        """Services with dependencies have depends_on configured."""
        from sonnet_cli.templates import render_docker_compose

        result = render_docker_compose(
            services=["pgduckdb", "pgadmin"],
            config={"project_name": "test_project"},
        )
        compose = yaml.safe_load(result)
        # pgadmin depends on pgduckdb
        assert "depends_on" in compose["services"]["pgadmin"]
        assert "pgduckdb" in compose["services"]["pgadmin"]["depends_on"]

    def test_render_docker_compose_creates_volumes(self):
        """Compose file includes required volume definitions."""
        from sonnet_cli.templates import render_docker_compose

        result = render_docker_compose(
            services=["pgduckdb"],
            config={"project_name": "test_project"},
        )
        compose = yaml.safe_load(result)
        assert "volumes" in compose
        assert "pgduckdb_data" in compose["volumes"]

    def test_render_docker_compose_excludes_unselected_dependencies(self):
        """Dependencies not in selected services are excluded from depends_on."""
        from sonnet_cli.templates import render_docker_compose

        # pipelinebase depends on pgduckdb and minio
        # but if minio not selected, it should be excluded
        result = render_docker_compose(
            services=["pgduckdb", "pipelinebase"],
            config={"project_name": "test_project"},
        )
        compose = yaml.safe_load(result)
        # pipelinebase should only depend on pgduckdb (minio not selected)
        deps = compose["services"]["pipelinebase"].get("depends_on", {})
        assert "pgduckdb" in deps
        assert "minio" not in deps

    def test_render_docker_compose_with_all_services(self):
        """Compose file handles all services correctly."""
        from sonnet_cli.templates import render_docker_compose

        result = render_docker_compose(
            services=[
                "pgduckdb",
                "pgadmin",
                "cloudbeaver",
                "minio",
                "jupyterbase",
                "pipelinebase",
                "dbtbase",
            ],
            config={"project_name": "full_stack"},
        )
        compose = yaml.safe_load(result)
        assert len(compose["services"]) == 7


class TestRenderEnvFile:
    """Tests for render_env_file function."""

    def test_render_env_file_includes_postgres_config(self):
        """Env file includes PostgreSQL configuration."""
        from sonnet_cli.templates import render_env_file

        result = render_env_file(
            services=["pgduckdb"],
            config={"project_name": "test_project"},
        )
        assert "POSTGRES_USER" in result
        assert "POSTGRES_PASSWORD" in result
        assert "POSTGRES_DB" in result

    def test_render_env_file_includes_minio_when_selected(self):
        """Env file includes MinIO config when minio is selected."""
        from sonnet_cli.templates import render_env_file

        result = render_env_file(
            services=["pgduckdb", "minio"],
            config={"project_name": "test_project"},
        )
        assert "MINIO_ROOT_USER" in result
        assert "MINIO_ROOT_PASSWORD" in result

    def test_render_env_file_excludes_minio_when_not_selected(self):
        """Env file excludes MinIO config when minio not selected."""
        from sonnet_cli.templates import render_env_file

        result = render_env_file(
            services=["pgduckdb", "pgadmin"],
            config={"project_name": "test_project"},
        )
        assert "MINIO_ROOT_USER" not in result

    def test_render_env_file_includes_pgadmin_when_selected(self):
        """Env file includes pgAdmin config when pgadmin is selected."""
        from sonnet_cli.templates import render_env_file

        result = render_env_file(
            services=["pgduckdb", "pgadmin"],
            config={"project_name": "test_project"},
        )
        assert "PGADMIN_DEFAULT_EMAIL" in result


class TestRenderReadme:
    """Tests for render_readme function."""

    def test_render_readme_lists_all_services(self):
        """README lists all selected services."""
        from sonnet_cli.templates import render_readme

        result = render_readme(
            services=["pgduckdb", "pgadmin"],
            project_name="test_project",
        )
        assert "pgduckdb" in result
        assert "pgadmin" in result
        assert "test_project" in result

    def test_render_readme_includes_connection_info(self):
        """README includes connection information."""
        from sonnet_cli.templates import render_readme

        result = render_readme(
            services=["pgduckdb", "pgadmin"],
            project_name="test_project",
        )
        assert "postgresql://" in result or "5432" in result
        assert "8080" in result or "localhost" in result

    def test_render_readme_includes_quick_start(self):
        """README includes quick start commands."""
        from sonnet_cli.templates import render_readme

        result = render_readme(
            services=["pgduckdb"],
            project_name="test_project",
        )
        assert "sonnet up" in result
        assert "sonnet down" in result


class TestRenderInitSql:
    """Tests for render_init_sql function."""

    def test_render_init_sql_includes_project_name(self):
        """Init SQL includes project name in comments."""
        from sonnet_cli.templates import render_init_sql

        result = render_init_sql(project_name="test_project")
        assert "test_project" in result

    def test_render_init_sql_creates_sample_schema(self):
        """Init SQL creates sample schemas."""
        from sonnet_cli.templates import render_init_sql

        result = render_init_sql(project_name="test_project")
        assert "CREATE SCHEMA" in result or "CREATE TABLE" in result


class TestRenderPgadminConfig:
    """Tests for render_pgadmin_config function."""

    def test_render_pgadmin_servers_json(self):
        """Generates valid servers.json for pgAdmin."""
        from sonnet_cli.templates import render_pgadmin_servers_json

        result = render_pgadmin_servers_json(project_name="test_project")
        import json

        config = json.loads(result)
        assert "Servers" in config
        assert "1" in config["Servers"]
        assert config["Servers"]["1"]["Host"] == "pgduckdb"

    def test_render_pgadmin_preferences_json(self):
        """Generates valid preferences.json for pgAdmin."""
        from sonnet_cli.templates import render_pgadmin_preferences_json

        result = render_pgadmin_preferences_json()
        import json

        config = json.loads(result)
        # Should be valid JSON
        assert isinstance(config, dict)

    def test_render_pgadmin_pgpass(self):
        """Generates valid pgpass file for pgAdmin."""
        from sonnet_cli.templates import render_pgadmin_pgpass

        result = render_pgadmin_pgpass()
        # pgpass format: hostname:port:database:username:password
        assert "pgduckdb:5432:postgres:postgres:postgres" in result
