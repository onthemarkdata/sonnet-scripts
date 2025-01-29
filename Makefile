# Set up the project with Docker Compose
setup:
	@docker compose build
	@docker compose up -d

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

load-db:
	@docker compose exec pythonbase python /apps/ingest_claims/load_claims_to_db.py

verify-db:
	@docker compose exec pgduckdb psql -U postgres -d postgres -c "SELECT COUNT(*) FROM raw_claims;"

# # Execute a shell inside the linuxbase container
# exec-linuxbase:
# 	@docker compose exec linuxbase bash

# Check the running containers
status:
	@docker compose ps

# Clean up containers, volumes, and images
clean:
	@docker compose down -v --rmi all --remove-orphans

# Run all tests inside the container
test:
	@docker compose exec pythonbase pytest /apps/tests

# Run only unit tests
test-unit:
	@docker compose exec pythonbase pytest /apps/tests/unit

# Run only integration tests
test-integration:
	@docker compose exec pythonbase pytest /apps/tests/integration