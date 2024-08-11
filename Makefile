#!make
include system.env

# Docker related commands
build-tank-app:
	docker build --tag ${IMAGE_NAME}:${IMAGE_TAG} --tag ${IMAGE_NAME}:latest -f ./tank/tank.Dockerfile .

build-tank-server-app:
	docker build --tag ${IMAGE_SERVER_NAME}:${IMAGE_SERVER_TAG} --tag ${IMAGE_SERVER_NAME}:latest -f ./tank/tank_server.Dockerfile .

build-tank-gui-app:
	docker build --tag ${IMAGE_GUI_NAME}:${IMAGE_GUI_TAG} --tag ${IMAGE_GUI_NAME}:latest -f ./tank/tank_gui.Dockerfile .


# Docker compose define targets
all-compose: up

up:
	docker-compose -f $(COMPOSE_FILE) --env-file system.env up -d

down:
	docker-compose -f $(COMPOSE_FILE) --env-file system.env down

clean:
	docker-compose -f $(COMPOSE_FILE) --env-file system.env down -v

re-create:
	docker-compose -f $(COMPOSE_FILE) --env-file system.env up -d --force-recreate

config:
	docker-compose -f $(COMPOSE_FILE) --env-file system.env config
# Help target
help:
	@echo "Available targets:"
	@echo "  all      Run the Docker Compose service"
	@echo "  up      Run the Docker Compose service in detached mode"
	@echo "  down    Stop and remove the Docker Compose service"
	@echo "  clean   Remove all Docker Compose containers and volumes"
	@echo "  help    Show this help message"