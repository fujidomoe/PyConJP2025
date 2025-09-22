DOCKER_COMPOSE := docker compose

docker/start:
	$(DOCKER_COMPOSE) up -d

docker/re-setup:
	$(DOCKER_COMPOSE) build --no-cache
	$(DOCKER_COMPOSE) up -d

gen/lock:
	uv pip compile pyproject.toml --group dev -o requirements-dev.lock
