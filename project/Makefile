all: 
	migration create_superuser up

migrate:
	python3 manage.py makemigrations && python3 manage.py migrate

up:
	docker-compose up --build

down:
	docker-compose down
	@echo " o projeto..."

createsuperuser:
	echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'pass')" | python3 manage.py shell
	@echo "super user criado..."

setup: down up migrate createsuperuser
	@echo "setup completo."

flush:
	python3 manage.py flush

.PHONY: migrate up down createsuperuser setup