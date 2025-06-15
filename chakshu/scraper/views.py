from core.logger import setup_logger

from .content_scraper import WikipediaScraper
from .table_scraper import WikipediaTableProcessor

logger = setup_logger(__name__)


def get_short_description(url):
    scraper = WikipediaScraper()
    soup = scraper.fetch_wikipedia_content(url)

    return scraper.fetch_short_description(soup)


def get_citations(url):
    scraper = WikipediaScraper()
    scraper.main(url)

    return scraper.citations


def get_full_content(url):
    scraper = WikipediaScraper()
    response = scraper.main(url)

    return response


def get_image_urls(url):
    scraper = WikipediaScraper()
    scraper.main(url)
    image_urls = scraper.images

    return image_urls


def get_tables(url):
    """
    Process Wikipedia tables from the given URL using Qwen2.5-VL.

    Args:
        url (str): URL of the Wikipedia article to process

    Returns:
        dict: Processing results including tables found and analysis, or None if failed
    """
    logger.info("Starting Wikipedia table processing", extra={"url": url})
    processor = None

    try:
        processor = WikipediaTableProcessor()
        result = processor.process_wikipedia_article_complete(article_url=url, save_screenshots=False)

        logger.info(
            "Wikipedia table processing completed",
            extra={
                "url": result.get("url"),
                "tables_found": result.get("tables_found", 0),
                "successful_analyses": result.get("successful_analyses", 0),
                "failed_analyses": result.get("failed_analyses", 0),
            },
        )

        if result.get("analyses"):
            try:
                processor.vision_analyzer.save_results_to_file(result["analyses"])
                logger.debug("Successfully saved analysis results to file")
            except Exception as save_error:
                logger.error("Failed to save analysis results", exc_info=save_error)

        return result
    except Exception:
        logger.error("Error processing Wikipedia tables", exc_info=True, extra={"url": url})
        return None
    finally:
        processor.close()
