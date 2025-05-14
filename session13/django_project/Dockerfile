FROM python:3.12-slim

WORKDIR /workspace

# Install Poetry
RUN pip install poetry

# Copy dependency files
COPY pyproject.toml poetry.lock /workspace/

# Install dependencies
RUN poetry install --no-root

# Copy the rest of the application code
COPY . .

# Expose the port
EXPOSE 8000

# Command to run the Django application
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
