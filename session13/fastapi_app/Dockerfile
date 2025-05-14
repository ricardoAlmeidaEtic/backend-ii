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
EXPOSE 8001

# Command to run the FastAPI application
CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
