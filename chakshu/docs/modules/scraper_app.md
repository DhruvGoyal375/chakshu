# Scraper App (`scraper`)

The `scraper` app is dedicated to fetching and parsing content from web pages, with a primary focus on Wikipedia articles.

## Responsibilities

* **Content Fetching**: Retrieving HTML content from given URLs.
* **HTML Parsing**: Extracting specific information from the HTML structure, such as:
    * Short descriptions
    * Full page text
    * Citations/references
    * Image URLs
* **Data Cleaning**: Potentially cleaning the extracted HTML or text content.

## Key Files and Components

* **`views.py`**:
    * This file contains helper functions that are called by other parts of the application (primarily `core.views`) to perform scraping tasks. It does not seem to define direct API endpoints for external use in the main workflow but rather service functions.
    * `get_short_description(url)`:
        * Instantiates `WikipediaScraper`.
        * Calls `scraper.fetch_wikipedia_content(url)` to get the page's `BeautifulSoup` object.
        * Calls `scraper.fetch_short_description(soup)` to extract the short description.
    * `get_citations(url)`:
        * Instantiates `WikipediaScraper`.
        * Calls `scraper.main(url)` (presumably this method initializes scraping and populates scraper instance attributes like `citations`).
        * Returns `scraper.citations`.
    * `get_full_content(url)`:
        * Instantiates `WikipediaScraper`.
        * Calls `scraper.main(url)` (or a similar method to get all content).
        * Returns the full content.
    * `get_image_urls(url)`:
        * Instantiates `WikipediaScraper`.
        * Calls `scraper.main(url)`.
        * Returns `scraper.images` (a list of image URLs).
    * `WikiSummaryScraper` (Class-Based View):
        * This view (`GET` method) seems to be a standalone utility to fetch and return a summary by scraping paragraphs directly. It's not used in the main `core.views.ProcessOptionView` flow for summaries (which uses `WikiAPI`). It might be for internal testing or an alternative approach.

* **`scraper.py` (Assumed Location)**:
    * This file is expected to contain the `WikipediaScraper` class, which is the core of the scraping logic.
    * **`WikipediaScraper` Class**:
        * `Workspace_wikipedia_content(url)`: Likely uses a library like `requests` to get the page HTML and `BeautifulSoup` to parse it.
        * `Workspace_short_description(soup)`: Implements logic to find and extract the short description element from the parsed HTML.
        * `main(url)`: A central method that likely orchestrates the fetching and parsing of various page elements (text, images, citations), storing them in instance attributes.
        * Other methods for cleaning HTML (`clean_html_tags`), extracting specific sections, etc.
    * *Developer Note: The implementation of `WikipediaScraper` is crucial. Developers should thoroughly understand its parsing logic, CSS selectors or XPath expressions used, and error handling for network issues or changes in Wikipedia's HTML structure.*

* **`imageScrapper.py`**:
    * The purpose of this file is distinct from `scraper.py`. It might contain specialized logic for finding image URLs or processing images in a way that `scraper.py` doesn't cover, or it could be an alternative image scraping mechanism. Its interaction with `WikipediaScraper` or other parts of the app needs to be determined by examining its content.

* **`models.py`**:
    * If the scraper needs to store fetched data persistently (e.g., for caching raw HTML, parsed sections), models would be defined here. The directory structure includes it, but no specific models are detailed in the provided context.

* **`urls.py`**:
    * The file structure shows `scraper/urls.py`. While not explicitly detailed, if this app exposes any direct API endpoints (e.g., for testing scraper functionalities independently), they would be defined here and included in `api/urls.py`.

## Dependencies

* **`requests` (likely)**: For making HTTP requests.
* **`BeautifulSoup4` (likely)**: For parsing HTML.

## Development Considerations

* **Robustness to HTML Changes**: Web scraping is fragile and can break if the target website's structure changes. The selectors used in `WikipediaScraper` should be as resilient as possible. Consider using more stable identifiers if available (e.g., `id` attributes, specific classes).
* **Rate Limiting/User-Agent**: When scraping websites, it's important to be respectful. Implement proper User-Agent strings. For Wikipedia, the MediaWiki API (`core.wiki_api.py`) is generally preferred for structured data to avoid stressing raw page loads. The scraper might be used for content not easily available via the API.
* **Error Handling**: Implement comprehensive error handling for network errors, timeouts, and parsing errors (e.g., when expected HTML elements are not found).
* **Maintainability**: Keep scraping logic well-organized and documented, especially the parts that rely on specific HTML structures.
* **Alternative Data Sources**: For Wikipedia, always consider if the MediaWiki API can provide the required information more reliably than scraping. The current setup uses a mix, which is a good approach.