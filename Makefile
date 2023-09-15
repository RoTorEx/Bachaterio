.ONESHELL:
py := poetry run
python := $(py) python
main_dir := src

code_dir = $(main_dir)


hello:
	@echo "Look for doc and entry correct argument."

clean:
	@find . -name \*__pycache__ -type d -exec rm -rf '{}' \;


# Linters
.PHONY: lint
lint:
	@$(py) isort $(code_dir)
	@$(py) black $(code_dir)
	@$(py) flake8 $(code_dir)
	# @$(py) mypy $(code_dir)


# Docker compose
.PHONY: up
up:
	@docker compose up -d --build

.PHONY: reup
reup:
	@docker compose down -v
	@docker compose up -d --build

.PHONY: down
down:
	@docker compose down -v

.PHONY: logs
logs:
	@docker compose logs -f

.PHONY: push
push:
	@docker buildx build \
	-t amsisid3/bachaterio:latest  \
	-f ./Dockerfile . \
	--platform=linux/amd64 \
	--push
