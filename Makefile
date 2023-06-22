dev:
	docker-compose -f docker/develop/fastapi/docker-compose.yml --project-directory . $(filter-out $@,$(MAKECMDGOALS))
