# Configuration Guide

This guide covers all configuration options for Chakshu, including environment variables, Django settings, external service configuration, and deployment-specific settings.

## Environment Variables

Chakshu uses environment variables for configuration to support different deployment environments and maintain security best practices.

### Core Django Settings

```env
# Basic Django Configuration
DEBUG=False
SECRET_KEY=your-production-secret-key-here-make-it-long-and-random
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database Configuration
DB_ENGINE=django.db.backends.postgresql
DB_NAME=chakshu_prod
DB_USER=chakshu_user
DB_PASSWORD=secure_password_here
DB_HOST=db
DB_PORT=5432

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=logs/chakshu.log
```

### External Service Configuration

```env
# Wikipedia API Settings
WIKI_USER_AGENT=Chakshu/1.0 (your-email@example.com)

# AI Services
OLLAMA_BASE_URL=http://ollama:11434
MODEL_NAME=qwen2.5vl

# LaTeX Processing Service
LATEX_TO_TEXT_BASE_URL=http://latex_to_text:3000

# Processing Settings
IMAGE_PROCESSING_TIMEOUT=90
TABLE_PROCESSING_TIMEOUT=120
MAX_CONCURRENT_IMAGES=5
```

### Security and CORS Settings

```env
# CORS Configuration
CORS_ORIGIN_ALLOW_ALL=False
CORS_ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Security Settings (Production)
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True
SECURE_CONTENT_TYPE_NOSNIFF=True
SECURE_BROWSER_XSS_FILTER=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### Caching Configuration

```env
# Cache Backend (Development - Local Memory)
CACHE_BACKEND=django.core.cache.backends.locmem.LocMemCache
CACHE_LOCATION=image_captions_cache
CACHE_TIMEOUT=86400

# Cache Backend (Production - Redis)
CACHE_BACKEND=django_redis.cache.RedisCache
CACHE_LOCATION=redis://redis:6379/1
CACHE_TIMEOUT=86400
```

## Configuration Files

### Environment File (.env)

Create a `.env` file in your project root:

```bash
# Copy the example file
cp .env.example .env

# Edit with your settings
nano .env
```

**Development Example**:
```env
DEBUG=True
SECRET_KEY=dev-key-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1

# Use SQLite for development
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3

# Local services
OLLAMA_BASE_URL=http://localhost:11434
LATEX_TO_TEXT_BASE_URL=http://localhost:3000

# Development logging
LOG_LEVEL=DEBUG
```

**Production Example**:
```env
DEBUG=False
SECRET_KEY=your-very-secure-production-key-here
ALLOWED_HOSTS=chakshu.yourdomain.com

# PostgreSQL for production
DB_ENGINE=django.db.backends.postgresql
DB_NAME=chakshu_prod
DB_USER=chakshu_user
DB_PASSWORD=secure_database_password
DB_HOST=db
DB_PORT=5432

# Production services
OLLAMA_BASE_URL=http://ollama:11434
LATEX_TO_TEXT_BASE_URL=http://latex_to_text:3000

# Production caching
CACHE_BACKEND=django_redis.cache.RedisCache
CACHE_LOCATION=redis://redis:6379/1

# Security settings
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True

# Production logging
LOG_LEVEL=INFO
```

## Django Settings Configuration

### Database Configuration

**SQLite (Development)**:
```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
```

**PostgreSQL (Production)**:
```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": get_env_variable("DB_NAME", "chakshu_prod"),
        "USER": get_env_variable("DB_USER", "chakshu_user"),
        "PASSWORD": get_env_variable("DB_PASSWORD"),
        "HOST": get_env_variable("DB_HOST", "localhost"),
        "PORT": get_env_variable("DB_PORT", "5432"),
    }
}
```

### Caching Configuration

**Local Memory Cache (Development)**:
```python
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "chakshu_cache",
        "TIMEOUT": 3600,
    }
}
```

**Redis Cache (Production)**:
```python
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/1",
        "TIMEOUT": 3600,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
```

### Logging Configuration

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'logs/chakshu.log',
            'maxBytes': 10*1024*1024,  # 10MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['file', 'console'],
        'level': get_env_variable('LOG_LEVEL', 'INFO'),
    },
}
```

## External Service Configuration

### Ollama (AI Service)

**Installation**:
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull the required model
ollama pull qwen2.5vl

# Start the service
ollama serve
```

**Configuration**:
```env
OLLAMA_BASE_URL=http://localhost:11434
MODEL_NAME=qwen2.5vl
IMAGE_PROCESSING_TIMEOUT=90
```

**Docker Configuration**:
```yaml
# docker-compose.yml
ollama:
  image: ollama/ollama:latest
  container_name: ollama
  ports:
    - "11434:11434"
  restart: unless-stopped
  volumes:
    - ollama_data:/root/.ollama
```

### LaTeX-to-Text Service

**Setup**:
```bash
cd latex_to_text
npm install
npm start
```

**Configuration**:
```env
LATEX_TO_TEXT_BASE_URL=http://localhost:3000
```

**Docker Configuration**:
```yaml
# docker-compose.yml
latex_to_text:
  build:
    context: .
    dockerfile: latex_to_text/Dockerfile
  container_name: latex_to_text
  ports:
    - "3000:3000"
  restart: unless-stopped
```

### Wikipedia API

**Configuration**:
```env
WIKI_USER_AGENT=Chakshu/1.0 (your-email@example.com)
```

**Rate Limiting**:
```python
# Built-in rate limiting for Wikipedia requests
RATE_LIMIT = "5/m"  # 5 requests per minute
```

## Performance Configuration

### Processing Limits

```env
# Image Processing
MAX_CONCURRENT_IMAGES=5
IMAGE_PROCESSING_TIMEOUT=90

# Table Processing
TABLE_PROCESSING_TIMEOUT=120
MAX_CONCURRENT_TABLES=3

# General Processing
REQUEST_TIMEOUT=30
MAX_RETRIES=3
```

### Cache Settings

```env
# Cache Timeouts (seconds)
SEARCH_CACHE_TIMEOUT=3600      # 1 hour
CONTENT_CACHE_TIMEOUT=3600     # 1 hour
IMAGE_CACHE_TIMEOUT=86400      # 24 hours
TABLE_CACHE_TIMEOUT=3600       # 1 hour
```

### Memory and Resource Limits

```env
# Memory limits for processing
MAX_MEMORY_PER_PROCESS=1GB
MAX_PROCESSING_TIME=300

# File size limits
MAX_IMAGE_SIZE=10MB
MAX_ARTICLE_SIZE=5MB
```

## Security Configuration

### Production Security Settings

```env
# SSL/HTTPS
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS=True
SECURE_HSTS_PRELOAD=True

# Content Security
SECURE_CONTENT_TYPE_NOSNIFF=True
SECURE_BROWSER_XSS_FILTER=True
X_FRAME_OPTIONS=DENY

# Cookies
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
CSRF_COOKIE_SECURE=True
CSRF_COOKIE_HTTPONLY=True
```

### API Security

```env
# Rate Limiting
RATE_LIMIT_SEARCH=5/m
RATE_LIMIT_PROCESS=3/m
RATE_LIMIT_GLOBAL=100/h

# Request Validation
MAX_QUERY_LENGTH=255
MAX_URL_LENGTH=500
ALLOWED_WIKIPEDIA_DOMAINS=en.wikipedia.org
```

## Docker Configuration

### docker-compose.yml

```yaml
version: '3.8'

services:
  chakshu:
    build:
      context: .
      dockerfile: chakshu/Dockerfile
    container_name: chakshu
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
      - OLLAMA_BASE_URL=http://ollama:11434
      - LATEX_TO_TEXT_BASE_URL=http://latex_to_text:3000
    depends_on:
      - ollama
      - latex_to_text
      - redis
    restart: unless-stopped

  ollama:
    image: ollama/ollama:latest
    container_name: ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    restart: unless-stopped

  latex_to_text:
    build:
      context: .
      dockerfile: latex_to_text/Dockerfile
    container_name: latex_to_text
    ports:
      - "3000:3000"
    restart: unless-stopped

  redis:
    image: redis:alpine
    container_name: redis
    ports:
      - "6379:6379"
    restart: unless-stopped

volumes:
  ollama_data:
```

### Environment-Specific Overrides

**docker-compose.override.yml** (Development):
```yaml
version: '3.8'

services:
  chakshu:
    environment:
      - DEBUG=True
      - LOG_LEVEL=DEBUG
    volumes:
      - .:/app
    command: python manage.py runserver 0.0.0.0:8000
```

**docker-compose.prod.yml** (Production):
```yaml
version: '3.8'

services:
  chakshu:
    environment:
      - DEBUG=False
      - LOG_LEVEL=INFO
    command: gunicorn chakshu.wsgi:application --bind 0.0.0.0:8000 --workers 3

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/ssl
    depends_on:
      - chakshu
```

## Configuration Validation

### Startup Checks

```python
def validate_configuration():
    """Validate configuration on startup."""
    required_vars = [
        'SECRET_KEY',
        'OLLAMA_BASE_URL',
        'WIKI_USER_AGENT',
    ]
    
    for var in required_vars:
        if not get_env_variable(var):
            raise RuntimeError(f"Required environment variable {var} is not set")
    
    # Test external services
    if not test_ollama_connection():
        logger.warning("Ollama service not available - image captioning disabled")
    
    if not test_latex_service():
        logger.warning("LaTeX service not available - math processing disabled")
```

### Configuration Testing

```bash
# Test configuration
python manage.py check

# Test database connection
python manage.py dbshell

# Test external services
curl http://localhost:11434/api/tags
curl http://localhost:3000/health
```

## Troubleshooting Configuration

### Common Issues

**Environment Variables Not Loading**:
```bash
# Check if .env file exists and is readable
ls -la .env
cat .env

# Verify environment variables are set
python -c "import os; print(os.getenv('DEBUG'))"
```

**Database Connection Issues**:
```bash
# Test PostgreSQL connection
psql -h localhost -U chakshu_user -d chakshu_prod

# Check Django database settings
python manage.py dbshell
```

**External Service Issues**:
```bash
# Test Ollama service
curl http://localhost:11434/api/tags

# Test LaTeX service
curl http://localhost:3000/health

# Check service logs
docker logs ollama
docker logs latex_to_text
```

### Configuration Debugging

```python
# Debug configuration loading
from core.utils import get_env_variable

print("DEBUG:", get_env_variable("DEBUG"))
print("OLLAMA_BASE_URL:", get_env_variable("OLLAMA_BASE_URL"))
print("DATABASE:", settings.DATABASES['default'])
```

## Next Steps

- **[Installation Guide](installation.md)** - Complete installation instructions
- **[API Documentation](api/index.md)** - API configuration and usage
- **[Project Structure](project_structure.md)** - Understanding the codebase