dev:
	./init.sh run --rm mercury_api bash

psql:
	PGPASSWORD=${POSTGRES_PASSWORD} psql -h ${POSTGRES_SERVER} -U ${POSTGRES_USER} -d ${POSTGRES_DB}

migrate:
	alembic upgrade head

up:
	uvicorn main:app --reload --workers 1 --host 0.0.0.0 --port 8080