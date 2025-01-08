.PHONY: setup build start stop update

# Full setup including building containers and initializing the project
setup: build start

# Build Docker containers
build:
	docker-compose build

# Start all services
start:
	docker-compose up -d

# Stop all services
stop:
	docker-compose down

# Sync Python dependencies with uv
update:
	docker-compose exec python-service uv sync