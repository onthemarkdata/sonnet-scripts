# Set up the project with Docker Compose
setup:
	@docker compose build linuxbase
	@docker compose build pythonbase
	@docker compose build
	@docker compose up -d

# Rebuild and start the containers (force rebuild)
rebuild:
	@docker compose build --no-cache
	@docker compose up -d

# Completely clean up Docker environment and rebuild containers from scratch
rebuild-clean:
	@docker compose down -v --remove-orphans --rmi all
	@docker compose build --no-cache linuxbase
	@docker compose build --no-cache pythonbase
	@docker compose build
	@docker compose up -d

# Stop the containers gracefully
stop:
	@docker compose down

# Execute a shell inside the pythonbase container
exec-pythonbase:
	@docker compose exec pythonbase bash

# Execute a PostgreSQL shell
exec-postgres:
	@docker compose exec pgduckdb psql -U postgres -d postgres

# Execute a DuckDB shell
exec-duckdb:
	@docker compose exec pythonbase /usr/local/bin/duckdb

# Execute a shell inside the linuxbase container
exec-linuxbase:
	@docker compose exec linuxbase bash

# Load data into PostgreSQL
load-db:
	@docker compose exec -e PYTHONPATH=/apps pythonbase /venv/bin/python -m ingest_claims.load_claims_to_db

# Verify data in PostgreSQL
verify-db:
	@docker compose exec pgduckdb psql -U postgres -d postgres -c "SELECT COUNT(*) FROM raw_claims;"

# Check the running containers
status:
	@docker compose ps

# Show logs of all containers or a specific one
logs:
	@docker compose logs -f $(c)

# Clean up containers, volumes, and images
clean:
	@docker compose down -v --rmi all --remove-orphans

# Backup the PostgreSQL database
backup-db:
	@docker compose exec pgduckdb pg_dump -U postgres -d postgres > backup.sql

# Restore the PostgreSQL database from a backup file
restore-db:
	@cat backup.sql | docker compose exec -T pgduckdb psql -U postgres -d postgres

# Run all tests inside the container
test:
	@docker compose exec -e PYTHONPATH=/apps pythonbase pytest -v /apps/tests

# Run only unit tests
test-unit:
	@docker compose exec -e PYTHONPATH=/apps pythonbase pytest /apps/tests/unit

# Run only integration tests
test-integration:
	@docker compose exec -e PYTHONPATH=/apps pythonbase pytest /apps/tests/integration

# Execute a pgAdmin GUI in localhost based on operating system
exec-pgadmin:
	@if [ "$$(docker compose exec pgduckdb psql -U postgres -d postgres -tAc "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public';" | tr -d '[:space:]')" = "0" ] || \
	    [ "$$(docker compose exec pgduckdb psql -U postgres -d postgres -tAc "SELECT SUM(reltuples)::int FROM pg_class WHERE relnamespace='public'::regnamespace AND relkind='r';" | tr -d '[:space:]')" = "0" ]; then \
		echo "No data tables or tables are empty. Loading data..."; \
		make load-db; \
	else \
		echo "Data already exists in PostgreSQL."; \
	fi
ifeq ($(shell uname),Darwin)
	open "http://pgadmin4%40pgadmin.org:password@localhost:8080"
else ifeq ($(OS),Windows_NT)
	powershell Start-Process "http://pgadmin4%40pgadmin.org:password@localhost:8080"
else
	xdg-open "http://pgadmin4%40pgadmin.org:password@localhost:8080"
endif
