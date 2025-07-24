import base64
import os
import time

import requests
from config import TABLE_ACCESSIBILITY_PROMPT, TABLE_SCREENSHOT_PATH
from core.logger import setup_logger
from core.utils import get_env_variable
from playwright.sync_api import sync_playwright

# Initialize logger
logger = setup_logger(__name__)


class PlaywrightTableCapture:
    def __init__(self):
        """Initialize Playwright browser"""

        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=True)
        self.page = self.browser.new_page()
        # Set viewport size
        self.page.set_viewport_size({"width": 1920, "height": 1080})

    def capture_tables(self, url, save_path=TABLE_SCREENSHOT_PATH):
        """Capture table screenshots using Playwright"""
        try:
            os.makedirs(save_path, exist_ok=True)

            # Navigate to page
            self.page.goto(url, wait_until="networkidle")

            # Find all tables
            tables = self.page.query_selector_all("table.wikitable, table.navbox")

            screenshot_paths = []

            for i, table in enumerate(tables):
                try:
                    # Scroll to table
                    table.scroll_into_view_if_needed()

                    # Take screenshot of the table element
                    filename = f"table_{i + 1}_{int(time.time())}.png"
                    filepath = os.path.join(save_path, filename)

                    table.screenshot(path=filepath)
                    screenshot_paths.append(filepath)

                    logger.info(f"Captured table {i + 1}: {filepath}")

                except Exception:
                    logger.error(f"Error capturing table {i + 1}", exc_info=True)
                    continue

            return screenshot_paths

        except Exception:
            logger.error("Error processing page", exc_info=True)
            return []

    def close(self):
        """Close browser and playwright"""
        self.browser.close()
        self.playwright.stop()


# Integration with Qwen2.5-VL via Ollama
class Qwen2VLIntegration:
    """
    Integration with Qwen2.5-VL running in Ollama, proxied by a FastAPI server.
    """

    def __init__(self):
        self.ollama_api_url = get_env_variable("OLLAMA_BASE_URL", "http://localhost:11434/api")
        self.model_name = get_env_variable("MODEL_NAME", "qwen2.5vl")
        self.table_analysis_prompt = TABLE_ACCESSIBILITY_PROMPT

    def encode_image_base64(self, image_path):
        """Convert image to base64 for API calls (kept for potential other uses)"""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")

    def process_table_with_qwen2vl(self, image_path, custom_prompt=None):
        """
        Sends a table image and a prompt to the FastAPI server as multipart/form-data.

        Args:
            image_path: Path to the table screenshot.
            custom_prompt: Optional custom prompt to override the default.

        Returns:
            A dictionary containing the analysis results.
        """
        prompt = custom_prompt if custom_prompt else self.table_analysis_prompt
        service_url = (
            f"{self.ollama_api_url}/query-file/"  # The log shows a double slash, ensure this is correct in your env var
        )

        logger.info(f"Analyzing table image via FastAPI proxy: {os.path.basename(image_path)}")

        try:
            # Prepare the multipart/form-data payload
            form_data = {"prompt": prompt}

            with open(image_path, "rb") as image_file:
                # The key 'file' must match the parameter name in the FastAPI endpoint
                files = {"file": (os.path.basename(image_path), image_file, "image/png")}

                # Make the API call using 'data' for form fields and 'files' for the file part
                response = requests.post(
                    service_url,
                    data=form_data,
                    files=files,
                    timeout=240,  # 4-minute timeout for vision processing
                )

            response.raise_for_status()

            result = response.json()
            analysis = result.get("response", "")

            return {
                "success": True,
                "analysis": analysis,
            }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": "Request timed out: The FastAPI server did not respond in time.",
            }
        except requests.exceptions.RequestException as e:
            error_message = f"Failed to communicate with the FastAPI server at {service_url}: {e}"
            if e.response is not None:
                error_message += f"\nResponse: {e.response.text}"
            return {
                "success": False,
                "error": error_message,
            }
        except Exception as e:
            return {"success": False, "error": f"An unexpected error occurred during processing: {e}"}

    def batch_analyze_tables(self, image_paths, custom_prompt=None):
        """
        Analyze multiple table images

        Args:
            image_paths: List of image file paths
            custom_prompt: Optional custom prompt for all images

        Returns:
            List of analysis results
        """
        results = []

        logger.info(f"Starting batch analysis of {len(image_paths)} table images...")

        for i, image_path in enumerate(image_paths, 1):
            logger.info(f"Processing image {i}/{len(image_paths)}: {os.path.basename(image_path)}")

            result = self.process_table_with_qwen2vl(image_path, custom_prompt)
            results.append(result)

            if result.get("success"):
                logger.debug(
                    f"Analysis result for {os.path.basename(image_path)}: {result.get('analysis', '')[:200]}..."
                )
            else:
                logger.warning(
                    f"Analysis failed for {os.path.basename(image_path)}: {result.get('error', 'Unknown error')}"
                )

        return results

    def save_results_to_file(self, results, output_file="table_analysis_results.txt"):
        """Save analysis results to a text file"""
        try:
            with open(output_file, "w", encoding="utf-8") as f:
                f.write("=== TABLE ANALYSIS RESULTS ===\n\n")

                for i, result in enumerate(results, 1):
                    f.write(f"--- TABLE {i} ---\n")
                    f.write(f"Image: {result.get('image_path', 'Unknown')}\n")
                    f.write(f"Status: {'Success' if result.get('success') else 'Failed'}\n")

                    if result.get("success"):
                        f.write(f"Model: {result.get('model', 'Unknown')}\n")
                        f.write(
                            f"Tokens - Prompt: {result.get('prompt_tokens', 0)}, Completion: {result.get('completion_tokens', 0)}\n"
                        )
                        f.write("\nANALYSIS:\n")
                        f.write(result.get("analysis", "No analysis available"))
                        f.write("\n")
                    else:
                        f.write(f"Error: {result.get('error', 'Unknown error')}\n")

                    f.write("\n" + "=" * 80 + "\n\n")

            logger.info(f"Results saved to: {output_file}")

        except Exception:
            logger.error("Error saving results", exc_info=True)


# Complete workflow integration
class WikipediaTableProcessor:
    """
    Complete workflow: Scrape → Screenshot → Analyze with Qwen2.5-VL
    """

    def __init__(self):
        # Initialize screenshot capture
        self.screenshot_capture = PlaywrightTableCapture()

        # Initialize Qwen2.5-VL integration
        self.vision_analyzer = Qwen2VLIntegration()

    def process_wikipedia_article_complete(self, article_url, save_screenshots=True):
        """
        Complete processing: screenshot tables and analyze with vision model

        Args:
            article_url: URL of Wikipedia article
            save_screenshots: Whether to keep screenshot files after analysis

        Returns:
            Dictionary with complete results
        """
        logger.info(f"Processing Wikipedia article: {article_url}")

        # Step 1: Capture table screenshots
        screenshot_paths = self.screenshot_capture.capture_tables(article_url)

        if not screenshot_paths:
            return {
                "url": article_url,
                "tables_found": 0,
                "screenshots": [],
                "analyses": [],
                "success": False,
                "message": "No tables found in the article",
            }

        logger.info(f"Found {len(screenshot_paths)} tables in the article")

        # Step 2: Analyze tables with Qwen2.5-VL
        analyses = self.vision_analyzer.batch_analyze_tables(screenshot_paths)

        # Step 3: Compile results
        result = {
            "url": article_url,
            "tables_found": len(screenshot_paths),
            "screenshots": screenshot_paths,
            "analyses": analyses,
            "success": True,
            "successful_analyses": sum(1 for a in analyses if a.get("success")),
            "failed_analyses": sum(1 for a in analyses if not a.get("success")),
        }

        # Step 4: Optionally clean up screenshot files
        if not save_screenshots:
            for path in screenshot_paths:
                try:
                    os.remove(path)
                except Exception:
                    pass
            result["screenshots"] = ["Screenshots deleted after analysis"]

        return result

    def close(self):
        """Clean up resources"""
        self.screenshot_capture.close()


def main(article_url):
    logger.info("Starting Wikipedia Table Processing with Qwen2.5-VL")

    processor = WikipediaTableProcessor()

    try:
        result = processor.process_wikipedia_article_complete(article_url=article_url, save_screenshots=False)

        if result:
            logger.info(
                f"Processing complete. Tables found: {result['tables_found']}, "
                f"Successful: {result['successful_analyses']}, "
                f"Failed: {result['failed_analyses']}"
            )

            if result["analyses"]:
                processor.vision_analyzer.save_results_to_file(result["analyses"])

            return result
        return None
    except Exception:
        logger.error("Error processing Wikipedia article", exc_info=True)
        return None
    finally:
        processor.close()
        logger.info("Processing completed and resources cleaned up")


if __name__ == "__main__":
    test_urls = [
        "https://en.wikipedia.org/wiki/List_of_countries_by_population",
        "https://en.wikipedia.org/wiki/World_Health_Organization",
        "https://en.wikipedia.org/wiki/Python_(programming_language)",
    ]
    main(test_urls[0])
