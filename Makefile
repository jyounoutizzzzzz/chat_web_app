# start up server
up:
	docker compose up

# start up as background task
upd:
	docker compose up -d

# stop server
down:
	docker compose down

# access to container's terminal
shell:
	docker compose exec app bash

# create docker image
build:
	docker compose build

# create new project
startproject:
	docker compose run --rm python3 manage.py startproject ${service} .

# create new app
startapp:
	docker compose run --rm app python3 manage.py startapp ${service} 

makemigrations:
	docker compose run --rm app python3 manage.py makemigrations

migrate:
	docker compose run --rm app python3 manage.py migrate

createsuperuser:
	docker compose run --rm app python3 manage.py createsuperuser
