# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Install PostgreSQL client and build tools
RUN apt-get update && apt-get install -y \
    libpq-dev gcc python3-dev musl-dev

RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    python3-dev \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install Poetry in one layer
RUN pip install --upgrade pip poetry

# Copy only the necessary files for dependency installation
COPY chakshu/pyproject.toml chakshu/README.md /app/

# Project initialization (First-time setup)
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Copy the rest of the application code
COPY chakshu /app/chakshu

# Run Django setup commands for the first time
RUN python chakshu/manage.py migrate \
    && python chakshu/manage.py collectstatic --noinput \
    && python chakshu/manage.py createsuperuser --noinput || echo "Superuser already exists"

# Run the application
CMD ["python", "chakshu/manage.py", "runserver", "0.0.0.0:8000"]
