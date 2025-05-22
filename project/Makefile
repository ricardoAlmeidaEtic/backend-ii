all: 
	migration create_superuser up

migrate:
	docker-compose exec web poetry run python manage.py makemigrations
	docker-compose exec web poetry run python manage.py migrate

up:
	docker compose up --build

build:
	docker compose build

down:
	docker-compose down
	@echo " o projeto..."

createsuperuser:
	docker-compose exec web poetry run python manage.py createsuperuser

setup: down up migrate createsuperuser
	@echo "setup completo."

flush:
	python3 manage.py flush

.PHONY: migrate up down createsuperuser setup