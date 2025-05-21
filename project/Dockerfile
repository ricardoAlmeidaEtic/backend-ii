FROM python:3.12-slim

RUN pip install poetry

WORKDIR /app

COPY . .

EXPOSE 8000

CMD poetry install && poetry run python manage.py runserver --traceback 0.0.0.0:8000