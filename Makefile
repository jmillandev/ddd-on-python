dev:
	./init.sh run --rm mercury_api bash

psql:
	PGPASSWORD=${POSTGRES_PASSWORD} psql -h ${POSTGRES_SERVER} -U ${POSTGRES_USER} -d ${POSTGRES_DB}

migrate:
	alembic upgrade head