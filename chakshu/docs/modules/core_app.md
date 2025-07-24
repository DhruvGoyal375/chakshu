# Core App (`core`)

The `core` app is central to the Chakshu application's functionality. It orchestrates the main business logic, handles API requests for searching and processing Wikipedia articles, and interacts with other apps and external services.

## Responsibilities

* **API Endpoint Handling**: Defines and manages the primary API endpoints (`/search/`, `/select/`, `/process/`) through its views.
* **Workflow Orchestration**: Coordinates the flow of data and actions, such as receiving a search query, fetching results, allowing selection, and then delegating processing tasks to appropriate modules (scraper, captioner, WikiAPI).
* **External API Interaction**: Contains `wiki_api.py`, a dedicated client for communicating with the MediaWiki API to fetch structured data like page summaries.
* **Data Formatting**: Prepares and structures the JSON responses sent back to the client.

## Key Files and Components

* **`views.py`**:
    * `SearchResultsView`:
        * Handles `GET /api/search/`.
        * Takes a search query `q`.
        * Uses `googlesearch.search` to find Wikipedia articles.
        * Employs `joblib.Parallel` and `joblib.delayed` for concurrent fetching of short descriptions via `scraper.views.get_short_description`.
        * Formats and returns search results.
    * `SelectLinkView`:
        * Handles `GET /api/select/`.
        * Takes a Wikipedia article `link`.
        * Returns a predefined list of processing options.
    * `ProcessOptionView`:
        * Handles `GET /api/process/`.
        * Takes a `link` and a numeric `option`.
        * Acts as a dispatcher based on the `option`:
            * **Option 1 (Short Description)**: Calls `scraper.views.get_short_description()`.
            * **Option 2 (Summary)**: Calls `mediawiki_api.get_page_summary()` (from `core.wiki_api.WikiAPI`).
            * **Option 3 (Full Content)**: Calls `scraper.views.get_full_content()`.
            * **Option 4 (Image Captions)**: Calls `captioner.views.fetch_and_process_images()`.
            * **Option 5 (Citations)**: Calls `scraper.views.get_citations()`.
        * Formats and returns the processed data.

* **`urls.py`**:
    * Defines the URL patterns for the views mentioned above:
        * `path("search/", SearchResultsView.as_view(), name="search_results")`
        * `path("select/", SelectLinkView.as_view(), name="select_link")`
        * `path("process/", ProcessOptionView.as_view(), name="process_option")`
    * These URLs are included under the `/api/` namespace via `api/urls.py`.

* **`wiki_api.py`**:
    * Contains the `WikiAPI` class.
    * This class is responsible for making requests to the MediaWiki API (e.g., `action=query&format=json&prop=extracts&exintro=true&explaintext=true` for summaries).
    * The instance `mediawiki_api = WikiAPI(user_agent="Chakshu (chakshu@pec.edu.in)")` is used by `ProcessOptionView`.
    * *Developer Note: The exact implementation details of `WikiAPI` (methods, error handling, request construction) should be examined by developers working on this module.*

* **`models.py`**:
    * The provided file structure shows `models.py`. While the views don't explicitly interact with `core` models in the snippets, this file would define any database tables specific to the `core` app's needs (e.g., logging API requests, storing user preferences if features expand).
    * The migrations history (`0001_initial` to `0008_delete_imagecaption_delete_wikipediapage`) indicates that models related to `WikipediaImageCaption`, `ImageCaption`, and `WikipediaPage` have existed in this app at various points. Developers should check the current `models.py` to understand the active data schema.

* **`hyperlinks.py`**:
    * The purpose and content of this file are unknown from the provided information. It might contain utility functions for manipulating or generating URLs.

## Interaction with Other Modules

* **`scraper` app**: `core.views` calls functions in `scraper.views` to get scraped data like short descriptions, full content, and citations.
* **`captioner` app**: `core.views` calls `captioner.views.fetch_and_process_images` for image captioning.

## Development Considerations

* **Error Handling**: Ensure robust error handling within views, especially for external calls (Google Search, WikiAPI, other apps).
* **Performance**: The use of `joblib` in `SearchResultsView` is a good practice. Evaluate other areas for potential performance bottlenecks, especially in `ProcessOptionView` when dealing with large pages or many images.
* **Extensibility**: Design views and services in a way that allows new processing options or data sources to be added with relative ease.
* **Configuration**: API keys or sensitive parameters for external services (like a more specific User-Agent for WikiAPI if needed) should ideally be managed via `settings.py` or `config.py` rather than being hardcoded.