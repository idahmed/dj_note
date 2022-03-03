help:
	@echo "docker-compose commands:"
	@echo "	   make build:		Build (usually, requires to build when changes happen to the Dockerfile or docker-compose.yml)"
	@echo "    make run_uwsgi: 	Up app service"
	@echo "    make up: 		Up all services - Starts all services"
	@echo "	   make restart:    Restart (removes all services and restart them -- without rebuilding)"
	@echo "    make bash: 		Bash into application container"
	@echo "    make ps:			List containers/services"
	@echo "    make rm: 		Removes all docker containers running"
	@echo "    make rm_all: 	Removes all docker containers running"
	@echo "    make lint:       Run pre-commit hooks"
	@echo "    make mypy: 		Run typing checks"
	@echo "    make test: 		Run application unit tests"
	@echo "    make integration_test: 		run integration unit tests"
	@echo "    make db_backup: 		run database backup and restore script"

lint:
	docker-compose run --rm app pre-commit run --all-files

rm:
	docker-compose down && docker-compose rm -f

rm_all:
	docker rm -f $(docker ps -aq)

up:
	docker-compose up init && docker-compose up -d

ps:
	docker-compose ps

restart:
	make rm && make up

build:
	docker-compose build

bash:
	docker-compose run --rm app bash

test:
	docker-compose run --rm app pytest

integration_test:
	docker-compose run --rm app pytest -m integration

run_uwsgi:
	python manage.py collectstatic --no-input -v 0 && uwsgi --http :8000 --enable-threads --http-keepalive --processes 4 --wsgi-file config/wsgi.py --check-static /public_assets --static-map /static=/public_assets --static-map /media=/app/media --static-map /favicon.ico=/public_assets/favicon.ico --logto /dev/stdout --logto2 /dev/stderr --mimefile /etc/mime.types

mypy:
	docker-compose run --rm app mypy note_core

migrations:
	docker-compose run --rm app python manage.py makemigrations

migrate:
	docker-compose run --rm app python manage.py migrate

resetmigrations:
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	find . -path "*/migrations/*.pyc"  -delete
db_backup:
	./scripts/db_backups.sh