# Installation Guide

This guide provides detailed installation instructions for Chakshu, including development setup, Docker deployment, and production configuration.

## Prerequisites

Before installing Chakshu, ensure you have the following installed:

### Required Software
- **Python 3.10+** - [Download Python](https://www.python.org/downloads/)
- **Poetry** - [Install Poetry](https://python-poetry.org/docs/#installation)
- **Git** - [Install Git](https://git-scm.com/downloads)

### Optional (for full functionality)
- **Docker & Docker Compose** - [Install Docker](https://docs.docker.com/get-docker/)
- **Node.js 18+** - For LaTeX rendering service
- **Ollama** - For AI image captioning

## Development Installation

### 1. Clone the Repository

```bash
git clone https://github.com/DhruvGoyal375/chakshu.git
cd chakshu
```

### 2. Configure Poetry

Set up Poetry to create virtual environments within the project directory:

```bash
poetry config virtualenvs.in-project true
```

### 3. Install Dependencies

Install all Python dependencies using Poetry:

```bash
poetry install
```

This will create a virtual environment and install all required packages including development dependencies.

### 4. Activate Virtual Environment

```bash
poetry shell
```

### 5. Environment Configuration

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit the `.env` file with your configuration:

```env
# Basic Django settings
DEBUG=True
SECRET_KEY=your-development-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# External services (optional for basic functionality)
OLLAMA_BASE_URL=http://localhost:11434
LATEX_TO_TEXT_BASE_URL=http://localhost:3000
WIKI_USER_AGENT=Chakshu/1.0 (your-email@example.com)

# Logging
LOG_LEVEL=INFO
```

### 6. Database Setup

Run Django migrations to set up the database:

```bash
cd chakshu
python manage.py migrate
```

### 7. Start the Development Server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

## Docker Installation

For a complete setup with all services, use Docker Compose:

### 1. Clone and Navigate

```bash
git clone https://github.com/DhruvGoyal375/chakshu.git
cd chakshu
```

### 2. Build and Start Services

```bash
docker-compose up --build
```

This will start:
- **Chakshu Django app** on port 8000
- **Ollama service** on port 11434
- **LaTeX-to-text service** on port 3000

### 3. Access the Application

- API: `http://localhost:8000/api/`
- Documentation: `http://localhost:8000/docs/` (if configured)

## Service Dependencies Setup

### Ollama (AI Image Captioning)

1. **Install Ollama:**
   ```bash
   curl -fsSL https://ollama.ai/install.sh | sh
   ```

2. **Pull the Qwen2.5-VL model:**
   ```bash
   ollama pull qwen2.5vl
   ```

3. **Start Ollama service:**
   ```bash
   ollama serve
   ```

### LaTeX-to-Text Service

1. **Navigate to the service directory:**
   ```bash
   cd latex_to_text
   ```

2. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

3. **Start the service:**
   ```bash
   npm start
   ```

## Production Installation

### 1. Server Requirements

**Minimum Requirements:**
- 4 CPU cores
- 8GB RAM
- 50GB storage
- Ubuntu 20.04+ or similar Linux distribution

**Recommended for AI features:**
- 8+ CPU cores
- 16GB+ RAM
- GPU support for faster AI processing

### 2. System Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install system dependencies
sudo apt install -y python3.10 python3.10-venv python3-pip git nginx postgresql postgresql-contrib redis-server

# Install Docker (optional)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

### 3. Application Setup

```bash
# Create application user
sudo useradd -m -s /bin/bash chakshu
sudo su - chakshu

# Clone repository
git clone https://github.com/DhruvGoyal375/chakshu.git
cd chakshu

# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install --no-dev
```

### 4. Database Configuration

```bash
# Create PostgreSQL database
sudo -u postgres createdb chakshu_prod
sudo -u postgres createuser chakshu_user
sudo -u postgres psql -c "ALTER USER chakshu_user WITH PASSWORD 'secure_password';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE chakshu_prod TO chakshu_user;"
```

### 5. Environment Configuration

Create production `.env` file:

```env
DEBUG=False
SECRET_KEY=your-very-secure-production-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=chakshu_prod
DB_USER=chakshu_user
DB_PASSWORD=secure_password
DB_HOST=localhost
DB_PORT=5432

# Cache
CACHE_BACKEND=django_redis.cache.RedisCache
CACHE_LOCATION=redis://127.0.0.1:6379/1

# Security
SECURE_SSL_REDIRECT=True
SECURE_HSTS_SECONDS=31536000
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### 6. Static Files and Database

```bash
# Collect static files
poetry run python chakshu/manage.py collectstatic --noinput

# Run migrations
poetry run python chakshu/manage.py migrate
```

### 7. Systemd Service

Create `/etc/systemd/system/chakshu.service`:

```ini
[Unit]
Description=Chakshu Django Application
After=network.target

[Service]
Type=exec
User=chakshu
Group=chakshu
WorkingDirectory=/home/chakshu/chakshu
ExecStart=/home/chakshu/chakshu/.venv/bin/gunicorn --chdir chakshu chakshu.wsgi:application --bind 127.0.0.1:8000 --workers 3
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl enable chakshu
sudo systemctl start chakshu
```

## Verification

### Test Basic Functionality

1. **Health Check:**
   ```bash
   curl http://localhost:8000/api/search/?q=test
   ```

2. **Search Test:**
   ```bash
   curl "http://localhost:8000/api/search/?q=Python"
   ```

3. **Content Processing Test:**
   ```bash
   curl "http://localhost:8000/api/select/?link=https://en.wikipedia.org/wiki/Python"
   ```

### Test AI Features (if configured)

1. **Image Captioning Test:**
   ```bash
   curl "http://localhost:8000/api/process/?link=https://en.wikipedia.org/wiki/Python&option=4"
   ```

2. **Table Analysis Test:**
   ```bash
   curl "http://localhost:8000/api/process/?link=https://en.wikipedia.org/wiki/Python&option=5"
   ```

## Troubleshooting

### Common Issues

**Port Already in Use:**
```bash
# Find process using port 8000
sudo lsof -i :8000
# Kill the process
sudo kill -9 <PID>
```

**Permission Errors:**
```bash
# Fix file permissions
sudo chown -R chakshu:chakshu /home/chakshu/chakshu
chmod +x start_server.sh
```

**Database Connection Issues:**
```bash
# Check PostgreSQL status
sudo systemctl status postgresql
# Restart if needed
sudo systemctl restart postgresql
```

**Poetry Issues:**
```bash
# Clear Poetry cache
poetry cache clear --all pypi
# Reinstall dependencies
poetry install --no-cache
```

### Getting Help

If you encounter issues:

1. Check the [Troubleshooting Guide](development/troubleshooting.md)
2. Review logs: `tail -f chakshu/logs/chakshu.log`
3. Open an issue on [GitHub](https://github.com/DhruvGoyal375/chakshu/issues)
4. Join our community discussions

## Next Steps

After installation:

1. **[Configuration Guide](configuration.md)** - Configure Chakshu for your needs
2. **[API Documentation](api/index.md)** - Learn how to use the API
3. **[Development Guide](development/contributing.md)** - Start contributing to Chakshu