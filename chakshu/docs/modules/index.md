# Modules Overview

The Chakshu project is organized into several Django apps, each responsible for a distinct set of functionalities. This modular design promotes separation of concerns and makes the codebase easier to manage and scale.

## Django Apps

The primary applications within this project are:

* **[Core App (`core`)](core_app.md)**:
    Handles the main API logic, orchestrates calls to other services/apps, and manages interactions with external APIs like the MediaWiki API. It defines the primary user-facing API endpoints.

* **[Scraper App (`scraper`)](scraper_app.md)**:
    Responsible for all web scraping activities. It contains the logic to fetch and parse content from Wikipedia pages, such as short descriptions, full text, and citations.

* **[Captioner App (`captioner`)](captioner_app.md)**:
    Dedicated to generating or retrieving captions for images found on web pages.

* **[API App (`api`)](api_app.md)**:
    Serves as a routing and namespacing layer for the project's API. It aggregates URL patterns from other apps like `core` and `scraper`.

## Inter-App Communication

The `core` app often acts as the central coordinator. For example, when a user requests to process a Wikipedia page, the `core.views.ProcessOptionView` will:

* Call functions from `scraper.views` to get scraped content.
* Call methods from `core.wiki_api.WikiAPI` (which is part of the `core` app but interacts with an external service) for summaries.
* Call functions from `captioner.views` to get image captions.

This layered approach allows each app to specialize in its domain while contributing to the overall functionality of the application.

## Exploring Further

For detailed information on each app, please refer to their respective pages:

* [Core App (`core`)](core_app.md)
* [Scraper App (`scraper`)](scraper_app.md)
* [Captioner App (`captioner`)](captioner_app.md)
* [API App (`api`)](api_app.md)