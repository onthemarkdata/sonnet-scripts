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

# Execute a DuckDB shell via python
exec-duckdb-python:
	@docker compose exec pythonbase /usr/local/bin/duckdb

# Runs the DuckDB container (not python)
run-duckdb:
	@docker compose up -d duckdb

# Execute DuckDB CLI inside the dedicated DuckDB container (interactive use)
exec-duckdb:
	@docker compose exec duckdb duckdb

# Execute DuckDB UI in localhost based on operating system
exec-duckdb-ui:
	@if [ "$$(docker compose ps duckdb --format json | grep -c '"State":"running"')" = "0" ]; then \
		echo "DuckDB container is not running. Starting container..."; \
		make run-duckdb; \
	else \
		echo "DuckDB container is already running."; \
	fi
ifeq ($(shell uname),Darwin)
	open "http://localhost:4213"
else ifeq ($(OS),Windows_NT)
	powershell Start-Process "http://localhost:4213"
else
	xdg-open "http://localhost:4213"
endif

# Execute a shell inside the linuxbase container
exec-linuxbase:
	@docker compose exec linuxbase bash

# Load data into PostgreSQL
load-db:
	@docker compose exec -e PYTHONPATH=/apps pythonbase /venv/bin/python -m ingest_claims.load_claims_to_db

# Verify data in PostgreSQL
verify-db:
	@docker compose exec pgduckdb psql -U postgres -d postgres -c "SELECT COUNT(*) FROM raw_claims;"

# Replicate data from PostrgreSQL to MinIO
load-db-postgres-to-minio:
	@echo "Exporting PostgreSQL → CSV..."
	docker compose exec pgduckdb psql -U postgres -d postgres \
	  -c "\COPY raw_claims TO '/tmp/raw_claims.csv' CSV HEADER"

	@echo "Transferring CSV to Pythonbase container..."
	docker compose cp pgduckdb:/tmp/raw_claims.csv ./raw_claims.csv
	docker compose cp ./raw_claims.csv pythonbase:/apps/raw_claims.csv

	@echo "Running DuckDB pipeline CSV → MinIO..."
	docker compose exec pythonbase /venv/bin/python /apps/etl_pipelines/duckdb_to_minio.py

	@echo "Cleaning up temporary CSV files..."
	rm ./raw_claims.csv
	docker compose exec pythonbase rm /apps/raw_claims.csv

	@echo "PostgreSQL → CSV → DuckDB → MinIO pipeline completed."

# Build entire data platform, load data, and run all pipelines
run-all-data-pipelines: \
	load-db \
	verify-db \
	load-db-postgres-to-minio

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
	@docker compose exec -e PYTHONPATH=/apps pythonbase /venv/bin/pytest -v /apps/tests

# Run only unit tests
test-unit:
	@docker compose exec -e PYTHONPATH=/apps pythonbase /venv/bin/pytest /apps/tests/unit

# Run only integration tests
test-integration:
	@docker compose exec -e PYTHONPATH=/apps pythonbase /venv/bin/pytest /apps/tests/integration