# Quick Start Guide

Get Chakshu up and running in just a few minutes! This guide covers the fastest way to start using Chakshu for development or testing.

## 🚀 5-Minute Setup

### Prerequisites
- Python 3.10+
- Poetry (Python package manager)

### Installation

1. **Clone and enter the project:**
   ```bash
   git clone https://github.com/DhruvGoyal375/chakshu.git
   cd chakshu
   ```

2. **Install dependencies:**
   ```bash
   poetry config virtualenvs.in-project true
   poetry install
   ```

3. **Start the server:**
   ```bash
   poetry shell
   python chakshu/manage.py runserver
   ```

🎉 **That's it!** Chakshu is now running at `http://localhost:8000`

## 🧪 Test Your Installation

Try these API calls to verify everything works:

### 1. Search for Articles
```bash
curl "http://localhost:8000/api/search/?q=Python"
```

### 2. Get Article Options
```bash
curl "http://localhost:8000/api/select/?link=https://en.wikipedia.org/wiki/Python"
```

### 3. Get Article Summary
```bash
curl "http://localhost:8000/api/process/?link=https://en.wikipedia.org/wiki/Python&option=2"
```

## 🔧 Basic Configuration

Create a `.env` file for basic configuration:

```env
DEBUG=True
SECRET_KEY=your-development-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
LOG_LEVEL=INFO
WIKI_USER_AGENT=Chakshu/1.0 (your-email@example.com)
```

## 🐳 Docker Quick Start

Prefer Docker? Use this one-liner:

```bash
git clone https://github.com/DhruvGoyal375/chakshu.git
cd chakshu
docker-compose up --build
```

This starts:
- Chakshu API on port 8000
- Ollama AI service on port 11434  
- LaTeX service on port 3000

## 📚 API Usage Examples

### Search Wikipedia Articles
```bash
# Search for articles about Italy
curl "http://localhost:8000/api/search/?q=Italy"
```

**Response:**
```json
{
  "status": "success",
  "message": "Select the article you want to read",
  "results": [
    {
      "id": 1,
      "url": "https://en.wikipedia.org/wiki/Italy",
      "title": "Italy",
      "short_description": "Country in Southern Europe"
    }
  ],
  "query": "Italy",
  "result_count": 1
}
```

### Get Processing Options
```bash
# Get available options for an article
curl "http://localhost:8000/api/select/?link=https://en.wikipedia.org/wiki/Italy"
```

**Response:**
```json
{
  "status": "success",
  "message": "Select an option",
  "options": [
    {"id": 1, "description": "Read short description of the page"},
    {"id": 2, "description": "Read summary of the page"},
    {"id": 3, "description": "Read the full page content"},
    {"id": 4, "description": "Read captions of images on the page"},
    {"id": 5, "description": "Read tables on the page"},
    {"id": 6, "description": "Read references and citations on the page"}
  ],
  "article_url": "https://en.wikipedia.org/wiki/Italy",
  "article_title": "Italy"
}
```

### Process Content
```bash
# Get article summary (option 2)
curl "http://localhost:8000/api/process/?link=https://en.wikipedia.org/wiki/Italy&option=2"
```

## 🎯 Content Processing Options

| Option | Description | Use Case |
|--------|-------------|----------|
| 1 | Short description | Quick overview |
| 2 | Page summary | Detailed introduction |
| 3 | Full content | Complete article |
| 4 | Image captions | Visual content descriptions |
| 5 | Table analysis | Data and statistics |
| 6 | References | Citations and sources |

## 🔍 What's Next?

Now that Chakshu is running, explore these features:

### **For Users:**
- **[API Documentation](api/index.md)** - Complete API reference
- **[Features Overview](features/content_processing.md)** - Learn about accessibility features

### **For Developers:**
- **[Full Installation Guide](installation.md)** - Production setup
- **[Architecture Overview](architecture/core_components.md)** - Technical deep dive
- **[Contributing Guide](development/contributing.md)** - Join the development

### **For Advanced Setup:**
- **[AI Features Setup](architecture/ai_integration.md)** - Enable image captioning
- **[Docker Deployment](deployment/docker.md)** - Production deployment
- **[Configuration Guide](configuration.md)** - Advanced settings

## 🆘 Need Help?

**Common Issues:**
- **Port 8000 in use?** Try `python chakshu/manage.py runserver 8001`
- **Poetry not found?** Install with `curl -sSL https://install.python-poetry.org | python3 -`
- **Python version issues?** Ensure you have Python 3.10+

**Get Support:**
- 📖 [Troubleshooting Guide](development/troubleshooting.md)
- 🐛 [Report Issues](https://github.com/DhruvGoyal375/chakshu/issues)
- 💬 [Community Discussions](https://github.com/DhruvGoyal375/chakshu/discussions)

---

**Ready to make Wikipedia more accessible?** Let's get started! 🌟
