migration:
	docker exec -it movies python3 manage.py migrate --settings=config.settings.production
static:
	docker exec -it movies python3 manage.py collectstatic --noinput --settings=config.settings.production
run:
	docker-compose up
data:
	docker exec -it movies bash -c "cd movies && python3 data_load.py"