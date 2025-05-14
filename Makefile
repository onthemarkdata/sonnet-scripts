# Set up the project with Docker Compose
setup:
	@docker compose build
	@docker compose up -d

# Open the pgAdmin interface in the default browser
pgadmin:
	@echo "Opening pgAdmin interface at http://localhost:5050"
	@open http://localhost:5050

# Rebuild and start the containers (force rebuild)
rebuild:
	@docker compose build --no-cache
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

# # Execute a DuckDB shell
exec-duckdb:
	@docker compose exec pythonbase ./duckdb

# Execute a shell inside the linuxbase container
exec-linuxbase:
	@docker compose exec linuxbase bash

# Load data into PostgreSQL
load-db:
	@docker compose exec -e PYTHONPATH=/apps pythonbase python -m ingest_claims.load_claims_to_db


# Verify data in PostgreSQL
verify-db:
	@docker compose exec pgduckdb psql -U postgres -d postgres -c "SELECT COUNT(*) FROM raw_claims;"

<<<<<<< Updated upstream
=======
# Information about connecting to PostgreSQL via pgAdmin
pgadmin-info:
	@echo "To connect to PostgreSQL in pgAdmin:"
	@echo "  1. Open http://localhost:5050 in your browser"
	@echo "  2. Login with admin@sonnet.com / admin"
	@echo "  3. Add a new server with these settings:"
	@echo "     - Name: pgduckdb"
	@echo "     - Host: pgduckdb"
	@echo "     - Port: 5432"
	@echo "     - Username: postgres"
	@echo "     - Password: postgres"
>>>>>>> Stashed changes

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