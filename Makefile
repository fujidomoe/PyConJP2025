DOCKER_COMPOSE := docker compose

docker/start:
	$(DOCKER_COMPOSE) up -d

docker/re-setup:
	$(DOCKER_COMPOSE) build --no-cache
	$(DOCKER_COMPOSE) up -d

gen/lock:
	uv pip compile pyproject.toml -o requirements.lock
	uv pip compile pyproject.toml --group dev -o requirements-dev.lock

curl/healthcheck:
	curl http://localhost:8080/healthcheck

curl/users/me:
	curl http://localhost:8080/v1/users/me
