# Welcome to Chakshu

**Chakshu** is an accessibility-focused Django web application that helps blind and visually impaired users navigate and consume Wikipedia content through voice commands and structured text output.

## What is Chakshu?

Chakshu transforms Wikipedia articles into accessible, screen-reader-friendly content by providing:

- **Voice-command navigation** for Wikipedia articles
- **AI-powered image descriptions** using advanced vision models
- **Structured content extraction** optimized for screen readers
- **Table analysis and description** for complex data
- **Mathematical content conversion** from LaTeX to readable text
- **Citation and reference extraction** for research purposes

## Key Features

### 🔍 **Smart Search & Navigation**
Search Wikipedia articles and get structured results with short descriptions for easy navigation.

### 🖼️ **AI Image Captioning**
Advanced computer vision generates detailed, accessibility-focused descriptions of all images on Wikipedia pages.

### 📊 **Table Processing**
Screenshots and analyzes complex Wikipedia tables, converting them to screen-reader-friendly descriptions.

### 🧮 **Mathematical Content**
Converts LaTeX equations and chemical formulas into readable text format for text-to-speech systems.

### 📚 **Comprehensive Content Access**
- Short descriptions and summaries
- Full article content with structured formatting
- References and citations
- Image captions and descriptions

## Quick Start

Get Chakshu running in minutes:

```bash
# Clone the repository
git clone https://github.com/DhruvGoyal375/chakshu.git
cd chakshu

# Install dependencies
poetry install

# Start the server
python chakshu/manage.py runserver
```

## API Overview

Chakshu provides a simple REST API with three main endpoints:

1. **Search**: `/api/search/?q={query}` - Find Wikipedia articles
2. **Select**: `/api/select/?link={url}` - Get processing options for an article
3. **Process**: `/api/process/?link={url}&option={1-6}` - Extract specific content types

## Getting Started

New to Chakshu? Start here:

1. **[Project Overview](project_overview.md)** - Understand Chakshu's mission and capabilities
2. **[Quick Start](setup_guide.md)** - Get up and running in minutes
3. **[API Documentation](api/index.md)** - Explore the REST API
4. **[Features](features/content_processing.md)** - Learn about accessibility features

## Architecture

Chakshu is built with modern technologies:

- **Django 5.1** with REST Framework
- **Ollama + Qwen2.5-VL** for AI image captioning
- **Playwright** for table screenshot capture
- **Docker** for containerized deployment
- **Poetry** for dependency management

## Contributing

Chakshu is an open-source project focused on digital accessibility. We welcome contributions that help make the web more accessible for visually impaired users.

To contribute:
1. Fork the repository on GitHub
2. Create a feature branch for your changes
3. Follow the existing code style and documentation standards
4. Submit a pull request with a clear description of your changes