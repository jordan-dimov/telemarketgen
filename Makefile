.DEFAULT_GOAL := build
.EXPORT_ALL_VARIABLES:

PYTHONPATH=.

.PHONY: format
format:
	poetry run ruff format .
	poetry run ruff check --fix .

.PHONY: lint
lint:
	poetry run ruff check .

.PHONY: test
test:
	poetry run pytest tests/

.PHONY: build
build: lint test

.PHONY: run
run:
	poetry run uvicorn api.app:app

.PHONY: docker-build
docker-build:
	docker build -t telemarketgen:latest .

.PHONY: docker-run
docker-run:
	docker run -p 8000:8000 --env-file .env telemarketgen:latest

