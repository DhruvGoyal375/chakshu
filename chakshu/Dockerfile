# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Upgrade pip and install Poetry in one layer
RUN pip install --upgrade pip poetry

# Copy only the necessary files for dependency installation
COPY chakshu/pyproject.toml chakshu/poetry.lock* chakshu/README.md /app/

# Project initialization
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Copy the rest of the application code
COPY chakshu /app/chakshu

# Run the application
CMD ["python", "chakshu/manage.py", "runserver", "0.0.0.0:8000"]
