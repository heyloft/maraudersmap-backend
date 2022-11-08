.DEFAULT_GOAL := help

.PHONY: help
help:
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: init
init: ## Initialize new development environment
	curl -sSL https://install.python-poetry.org | python3 -
	poetry config --local virtualenvs.in-project true
	poetry install
	poetry run pre-commit install
	cp maraudersmap/base.env maraudersmap/.env

.PHONY: vscode
vscode: ## Connect Poetry virtual environment to VSCode (WARNING: replaces .vscode/settings.json)
	VENV_PATH=$$(poetry env info -p) && VENV_EXEC_PATH=$$(poetry run which python) && mkdir -p .vscode && echo "{\n\t\"python.pythonPath\": \"$$VENV_PATH\",\n\t\"python.defaultInterpreterPath\": \"$$VENV_EXEC_PATH\"\n}" > .vscode/settings.json

.PHONY: db
db: ## Initialize and start database
	if !(docker volume ls -q --filter "name=maraudersmap-data" | grep -q .); then docker volume create maraudersmap-data; fi
	if docker ps -qa --filter "name=maraudersmap-pg" | grep -q .; then docker start maraudersmap-pg; else docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=password -v maraudersmap-data:/var/lib/postgresql/data --name maraudersmap-pg postgres:14.5; fi
	echo "Give db some time to warm up..." && sleep 4
	cd maraudersmap && poetry run alembic upgrade head
	docker attach maraudersmap-pg

.PHONY: dbshell
dbshell: ## Spawn psql shell for database
	docker exec -it maraudersmap-pg psql -U postgres

.PHONY: api
api: ## Start backend
	cd maraudersmap && poetry run uvicorn main:app --host 0.0.0.0 --reload

.PHONY: nukedb
nukedb: ## Tear down database
	if docker ps -q --filter "name=maraudersmap-pg" | grep -q .; then docker stop maraudersmap-pg; fi
	if docker ps -qa --filter "name=maraudersmap-pg" | grep -q .; then docker rm maraudersmap-pg; fi
	if docker volume ls -q --filter "name=maraudersmap-data" | grep -q .; then docker volume rm maraudersmap-data; fi

.PHONY: seed
seed: ## Inject sample data
	docker exec -i maraudersmap-pg /bin/bash -c "PGPASSWORD=password psql --username postgres postgres" < maraudersmap/database/seed.sql

.PHONY: dump
dump: ## Update seed dump
	docker exec -i maraudersmap-pg /bin/bash -c "PGPASSWORD=password pg_dump --exclude-table-data='alembic_version' --data-only --username postgres postgres" > maraudersmap/database/seed.sql
