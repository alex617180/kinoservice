docker-dev:
	docker-compose -f docker-compose.debug.yml up --build --force-recreate

docker-prod:
	docker-compose -d -f docker-compose.yml up --build