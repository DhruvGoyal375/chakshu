# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Upgrade pip
RUN pip install --upgrade pip

# Install Poetry
RUN pip install poetry

# Copy only requirements to cache them in docker layer
COPY pyproject.toml /app/

# Project initialization:
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copy project
COPY . /app/

# Run the application
CMD ["python", "chakshu/manage.py", "runserver", "0.0.0.0:8000"]