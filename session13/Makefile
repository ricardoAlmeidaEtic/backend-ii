# Start all services
up:
	docker-compose up -d
down:
	docker-compose down

build:
	docker-compose build
clean:
	docker-compose down --volumes --remove-orphans

logs:
	docker-compose logs -f

migrate:
	docker-compose run --rm django poetry run python manage.py migrate

createsuperuser:
	docker-compose run --rm django poetry run python manage.py createsuperuser
