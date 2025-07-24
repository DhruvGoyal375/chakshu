# Project Structure

The Chakshu project follows a standard Django project layout. Here's an overview of the key directories and files:

```
chakshu/
├── api/                      # Django app: Handles API routing and structure
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations/
│   ├── models.py             # Database models for the 'api' app (if any)
│   ├── tests.py
│   ├── urls.py               # URL routing for the 'api' app
│   └── views.py              # Views for the 'api' app (if any specific logic)
├── captioner/                # Django app: Responsible for image captioning
│   ├── admin.py
│   ├── apps.py
│   ├── image_captioner.py    # Core logic for image captioning
│   ├── __init__.py
│   ├── metadata_image_captioner.py # Alternative/additional captioning logic
│   ├── migrations/
│   ├── models.py             # Models for storing caption data (e.g., cached captions)
│   ├── tests.py
│   └── views.py              # Views/functions like fetch_and_process_images
├── chakshu/                  # Main Django project directory
│   ├── asgi.py               # ASGI config for asynchronous serving
│   ├── __init__.py
│   ├── settings.py           # Django project settings
│   ├── urls.py               # Root URL configuration for the project
│   └── wsgi.py               # WSGI config for synchronous serving
├── config.py                 # Custom configuration file (contents unknown)
├── core/                     # Django app: Core business logic and orchestration
│   ├── admin.py
│   ├── apps.py
│   ├── hyperlinks.py         # (Contents unknown, likely utility for links)
│   ├── __init__.py
│   ├── migrations/
│   ├── models.py             # Models for core entities (e.g., search history, pages)
│   ├── tests.py
│   ├── urls.py               # URL routing for the 'core' app API endpoints
│   ├── views.py              # Main API views (SearchResultsView, SelectLinkView, ProcessOptionView)
│   └── wiki_api.py           # Wrapper for MediaWiki API interactions
├── demo.py                   # Standalone demonstration script (contents unknown)
├── Dockerfile                # Instructions for building a Docker image
├── __init__.py               # Makes the root 'chakshu' a Python package
├── manage.py                 # Django's command-line utility
├── output.txt                # Generic output file (likely for temporary results or logs)
├── README.md                 # Project README file, usually contains overview and setup
└── scraper/                  # Django app: Handles web scraping, particularly from Wikipedia
    ├── admin.py
    ├── apps.py
    ├── imageScrapper.py      # Logic for scraping images (contents unknown)
    ├── __init__.py
    ├── migrations/
    ├── models.py             # Models for scraped data (if any)
    ├── scraper.py            # Core WikipediaScraper class logic
    ├── tests.py
    ├── urls.py               # URL routing for 'scraper' app (if any direct endpoints)
    └── views.py              # Helper views/functions for scraping tasks
└── summarizer/               # Django app: (Functionality to be inferred, likely text summarization)
    # (Expected files: models.py, views.py, etc.)
```

## Key Components

### Django Project (`chakshu/`)

- **`settings.py`**: Contains all project configurations, including `INSTALLED_APPS`, `MIDDLEWARE`, `DATABASES`, `CACHES`, `SECRET_KEY`, etc. This is a crucial file for understanding how the project is wired up.
- **`urls.py`**: The main URL router. It includes `admin.site.urls` and delegates API-related URLs to the `api` app (`api.urls`).

### Django Apps

- **`api`**:
  - Acts as a primary entry point or namespace for the API.
  - `api/urls.py` includes URLs from `core.urls` and `scraper.urls`. This suggests it might serve as an aggregator or API versioning layer.

- **`core`**:
  - Contains central API logic.
  - `core/views.py` has the main views that handle client requests for search, selection, and processing.
  - `core/urls.py` defines endpoints like `/search/`, `/select/`, and `/process/`.
  - `core/wiki_api.py` likely acts as a dedicated MediaWiki API client to fetch structured data.

- **`scraper`**:
  - Manages web scraping tasks, focused on Wikipedia.
  - `scraper/scraper.py` likely contains the `WikipediaScraper` implementation.
  - `scraper/views.py` defines helper functions like `get_short_description`, `get_citations`, and `get_full_content`, used by `core.views`.

- **`captioner`**:
  - Generates or retrieves image captions.
  - `captioner/image_captioner.py` and `captioner/metadata_image_captioner.py` contain the captioning logic.
  - `captioner/views.py` includes endpoints like `Workspace_and_process_images`, likely called by `core.views`.

- **`summarizer`**:
  - Present in `INSTALLED_APPS`, but specific functionality is not shown.
  - Presumably handles summarization of scraped text content.

### Other Important Files

- **`manage.py`**: Utility script for running commands such as `runserver`, `makemigrations`, and `migrate`.
- **`Dockerfile`**: Contains instructions to build a Docker image for the application.
- **`config.py`**: A custom config file — possibly contains API keys, paths, or constants.
- **`README.md`**: Project overview and setup instructions.
- **`demo.py`**: Possibly demonstrates a specific feature or flow without requiring the full server to run.

---

Understanding this structure will help developers navigate the codebase, debug issues efficiently, and contribute new features effectively.
