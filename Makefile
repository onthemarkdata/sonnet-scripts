# Set up the project with Docker Compose
setup:
	@docker compose ps pythonbase --format json | grep -q pythonbase || docker compose build pythonbase
	@docker compose build $$(docker compose config --services | grep -v pythonbase)
	@docker compose up -d

# Install the sonnet CLI tool
install-cli:
	@echo "Installing sonnet CLI..."
	@cd cli && uv pip install -e .
	@echo "Done! Run 'sonnet --help' to get started."

# Rebuild and start the containers (force rebuild)
rebuild:
	@docker compose build --no-cache
	@docker compose up -d

# Completely clean up Docker environment and rebuild containers from scratch
rebuild-clean:
	@docker compose down -v --remove-orphans --rmi all
	@docker compose build --no-cache pythonbase
	@docker compose build --no-cache pipelinebase
	@docker compose build --no-cache dbtbase
	@docker compose build
	@docker compose up -d

# Stop the containers gracefully
stop:
	@docker compose down

# Execute a shell inside the pythonbase container
exec-pythonbase:
	@docker compose exec pythonbase bash

# Execute a shell inside the pipelinebase container
exec-pipelinebase:
	@docker compose exec pipelinebase bash

# Execute a PostgreSQL shell
exec-postgres:
	@docker compose exec pgduckdb psql -U postgres -d postgres

# Execute DuckDB shell with persistent DB file
exec-duckdb:
	@docker compose exec pythonbase /usr/local/bin/duckdb /apps/sonnet.duckdb

# Execute a DuckDB shell
exec-duckdb-shell:
	@docker compose exec pythonbase /usr/local/bin/duckdb

# Start CloudBeaver and open the UI
exec-cloudbeaver:
	@echo "Starting CloudBeaver..."
	docker compose up -d cloudbeaver
	@echo "CloudBeaver is running at: http://localhost:8978 (admin/admin)"

ifeq ($(shell uname),Darwin)
	open "http://localhost:8978"
else ifeq ($(OS),Windows_NT)
	powershell Start-Process "http://localhost:8978"
else
	xdg-open "http://localhost:8978"
endif

# Load data into PostgreSQL
load-db:
	@docker compose exec -e PYTHONPATH=/apps pipelinebase /venv/bin/python -m ingest_claims.load_claims_to_db

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
	@docker compose exec -e PYTHONPATH=/apps pipelinebase /venv/bin/pytest -v /apps/tests

# Run only unit tests
test-unit:
	@docker compose exec -e PYTHONPATH=/apps pipelinebase /venv/bin/pytest /apps/tests/unit

# Run only integration tests
test-integration:
	@docker compose exec -e PYTHONPATH=/apps pipelinebase /venv/bin/pytest /apps/tests/integration

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

# Open Jupyter Lab GUI in localhost based on operating system
exec-jupyter:
ifeq ($(shell uname),Darwin)
	open "http://localhost:8888"
else ifeq ($(OS),Windows_NT)
	powershell Start-Process "http://localhost:8888"
else
	xdg-open "http://localhost:8888"
endif

# Replicate data from PostrgreSQL to MinIO
load-db-postgres-to-minio:
	@echo "Exporting PostgreSQL → CSV (limited sample)..."
	docker compose exec pgduckdb psql -U postgres -d postgres \
	  -c "\COPY (SELECT * FROM raw_claims LIMIT 100000) TO '/tmp/raw_claims.csv' CSV HEADER"

	@echo "Transferring CSV to Pipelinebase container..."
	docker compose cp pgduckdb:/tmp/raw_claims.csv ./raw_claims.csv
	docker compose cp ./raw_claims.csv pipelinebase:/apps/raw_claims.csv >/dev/null 2>&1

	@echo "Running DuckDB pipeline CSV → MinIO..."
	docker compose exec -e PYTHONPATH=/apps pipelinebase /venv/bin/python -m etl_pipelines.duckdb_to_minio

	@echo "Cleaning up temporary CSV files..."
	rm ./raw_claims.csv
	docker compose exec pipelinebase rm /apps/raw_claims.csv

	@echo "PostgreSQL → CSV → DuckDB → MinIO pipeline completed."

# Check status of minio database
check-minio:
	docker compose exec minio mc alias set local http://localhost:9000 admin password
	docker compose exec minio mc admin info local
	docker compose exec minio mc ls local
	docker compose exec minio sh -c '\
	for bucket in $$(mc ls local | tr -s " " | cut -d" " -f5); do \
		echo "\nBucket: $$bucket"; \
		mc ls local/$$bucket; \
	done'

# Import data from MinIO into DuckDB
load-db-minio-to-duckdb:
	@echo "Running MinIO → DuckDB pipeline..."
	@docker compose exec -e PYTHONPATH=/apps pipelinebase /venv/bin/python -c \
		"from etl_pipelines.minio_to_duckdb import import_minio_to_duckdb, setup_duckdb_minio_connection; \
		con = setup_duckdb_minio_connection(); \
		import_minio_to_duckdb(con, 'postgres-data', 'raw_claims.parquet', 'raw_claims'); \
		con.close()"
	@echo "MinIO → DuckDB pipeline completed successfully."

# Verify data imported into DuckDB
check-duckdb:
	@docker compose exec pipelinebase /usr/local/bin/duckdb /apps/my_database.duckdb \
		-c "SELECT COUNT(*) AS row_count FROM raw_claims;"

# Build entire data platform, load data, and run all pipelines
run-all-data-pipelines: \
	load-db \
	verify-db \
	load-db-postgres-to-minio \
	check-minio \
	load-db-minio-to-duckdb \
	check-duckdb

# =============================================================================
# dbt Commands
# =============================================================================

# Execute a shell inside the dbtbase container
exec-dbtbase:
	@docker compose exec dbtbase bash

# Run dbt debug to test connection
dbt-debug:
	@docker compose exec dbtbase /venv/bin/dbt debug --project-dir /apps/dbt_project

# Install dbt packages (dbt-utils, dbt-expectations)
dbt-deps:
	@docker compose exec dbtbase /venv/bin/dbt deps --project-dir /apps/dbt_project

# Run dbt models
dbt-run:
	@docker compose exec dbtbase /venv/bin/dbt run --project-dir /apps/dbt_project

# Run dbt tests
dbt-test:
	@docker compose exec dbtbase /venv/bin/dbt test --project-dir /apps/dbt_project

# Run dbt with full refresh (rebuild tables)
dbt-run-full-refresh:
	@docker compose exec dbtbase /venv/bin/dbt run --full-refresh --project-dir /apps/dbt_project

# Run complete dbt workflow (deps + run + test)
dbt-build:
	@docker compose exec dbtbase /venv/bin/dbt deps --project-dir /apps/dbt_project
	@docker compose exec dbtbase /venv/bin/dbt run --project-dir /apps/dbt_project
	@docker compose exec dbtbase /venv/bin/dbt test --project-dir /apps/dbt_project

# Run specific dbt model (usage: make dbt-run-model model=stg_claims)
dbt-run-model:
	@docker compose exec dbtbase /venv/bin/dbt run --select $(model) --project-dir /apps/dbt_project

# Compile dbt without running
dbt-compile:
	@docker compose exec dbtbase /venv/bin/dbt compile --project-dir /apps/dbt_project

# Generate dbt documentation
dbt-docs-generate:
	@docker compose exec dbtbase /venv/bin/dbt docs generate --project-dir /apps/dbt_project

# Verify dbt transformed data in DuckDB
verify-dbt:
	@docker compose exec dbtbase /usr/local/bin/duckdb /apps/dbt.duckdb \
		-c "SELECT 'staging.stg_claims' as model, COUNT(*) as row_count FROM staging.stg_claims UNION ALL SELECT 'marts.fct_claims_summary', COUNT(*) FROM marts.fct_claims_summary;"