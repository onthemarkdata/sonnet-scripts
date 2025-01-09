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

# # Execute a shell inside the linuxbase container
# exec-linuxbase:
# 	@docker compose exec linuxbase bash

# Check the running containers
status:
	@docker compose ps

# Clean up containers, volumes, and images
clean:
	@docker compose down -v --rmi all --remove-orphans


