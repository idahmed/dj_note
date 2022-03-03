## Developer Guide

The development environment can be managed either locally via pipenv or using docker and docker-compose..

## Prerequisite

- [Docker](https://docs.docker.com/install/)
- [docker-compose](https://docs.docker.com/compose/install/)
- [Heroku](https://devcenter.heroku.com/articles/heroku-cli#download-and-install)

## Makefile reference

```bash
# build (usually, requires to build when changes happen to the Dockerfile or docker-compose.yml)
$ make build

# start all services and dependencies
$ make up

# down and remove all services
$ make rm

# restart (removes all services and restart them -- without rebuilding)
$ make restart

# list services running/active services
$ make ps

# open bash console in the app service
$ make bash

# Run pre-commit to project base and apply formatting using docker-compose.
$ make lint

# run unit testing
$ make test
# alternatively, a developer can open bash in application container and
# directly execute test or any other command
$ make bash
bash-5.0# pytest

```

## Services

- _RestFUL API_: (http://127.0.0.1:8000)[http://127.0.0.1:8000]
- _PostgreSQL_: (http://127.0.0.1:5432)[http://127.0.0.1:5432]
