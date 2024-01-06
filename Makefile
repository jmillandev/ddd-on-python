dev:
	docker compose -f docker/develop/docker-compose.yml --project-directory . $(filter-out $@,$(MAKECMDGOALS))

psql:
	PGPASSWORD=${POSTGRES_PASSWORD} psql -h ${POSTGRES_SERVER} -U ${POSTGRES_USER} -d ${POSTGRES_DB}

migrate:
	alembic upgrade head