dev:
	@if [ -z "$(command)" ]; then \
		echo "No <command> specified. Defaulting to bash."; \
		echo "To specify a <command?, run 'make dev command=<command>'"; \
		command="bash"; \
	fi;
	echo "Running command: $(command)"
	./init.sh run --rm mercury_api $(command)

up:
	uvicorn apps.planner.backend.server:app --reload --workers 1 --host 0.0.0.0 --port 8080	

psql:
	PGPASSWORD=${POSTGRES_PASSWORD} psql -h ${POSTGRES_SERVER} -U ${POSTGRES_USER} -d ${POSTGRES_DB}

migrate:
	alembic upgrade head

test:
	make lint
	pytest -v

generate/migration:
	alembic revision -m "$(message)"

format:
	black .
	isort .

lint:
	flake8 .
	black --check .
	isort --check-only .
