import re
from collections import OrderedDict
from functools import wraps
from urllib.parse import unquote

from captioner.views import fetch_and_process_images
from core.logger import setup_logger
from core.utils import get_env_variable
from django.core.cache import cache
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from googlesearch import search
from joblib import Parallel, delayed
from rest_framework import status
from scraper.views import get_citations, get_full_content, get_short_description, get_tables

from .wiki_api import WikiAPI

# Initialize logger
logger = setup_logger(__name__)

# Get configuration from environment variables
WIKI_USER_AGENT = get_env_variable("WIKI_USER_AGENT", "Chakshu/1.0 (chakshu@example.com)")
CACHE_TIMEOUT = int(get_env_variable("CACHE_TIMEOUT", "3600"))  # 1 hour default

# Initialize WikiAPI with proper user agent from environment variables
mediawiki_api = WikiAPI(user_agent=WIKI_USER_AGENT)


def validate_query_param(param_name, required=True, max_length=None):
    """Decorator to validate query parameters."""

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            param_value = request.GET.get(param_name)
            if param_value is not None:
                param_value = unquote(param_value.strip())

            if required and not param_value:
                logger.warning(f"Missing required parameter: {param_name}")
                return JsonResponse(
                    {"status": "error", "message": f"Missing required parameter: {param_name}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if param_value and max_length and len(param_value) > max_length:
                logger.warning(
                    f"Parameter {param_name} too long: {len(param_value)} characters. Max allowed: {max_length}"
                )
                return JsonResponse(
                    {"status": "error", "message": f"{param_name} is too long (max {max_length} characters)"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Store the validated and unquoted param in request for easier access in view
            if param_value is not None:
                request.validated_params = getattr(request, "validated_params", {})
                request.validated_params[param_name] = param_value

            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator


class SearchResultsView(View):
    @method_decorator(validate_query_param("q", required=True, max_length=255))
    def get(self, request):
        """Handle GET request for searching Wikipedia articles."""
        query = request.validated_params["q"]
        logger.info(f"Search request received for query: '{query}' from IP: {request.META.get('REMOTE_ADDR')}")

        cache_key = f"search_results:{query.lower().replace(' ', '_')}"
        cached_results = cache.get(cache_key)
        if cached_results:
            logger.info(f"Serving search results from cache for query: '{query}'")
            return JsonResponse(cached_results)

        try:
            query_for_wiki = f"{query} site:en.wikipedia.org"
            # Using advanced=True to get more structured results if available from the library
            search_results_objects = list(search(query_for_wiki, num_results=5, advanced=True))
            logger.info(f"Found {len(search_results_objects)} raw search results for query: '{query}'")

            if not search_results_objects:
                return JsonResponse(
                    {
                        "status": "success",
                        "message": "No results found.",
                        "results": [],
                        "query": query,
                        "result_count": 0,
                    },
                    status=status.HTTP_200_OK,
                )

            # Extract URLs and remove duplicates while maintaining order
            # Assuming search_results_objects are objects with a 'url' attribute
            unique_urls = list(OrderedDict.fromkeys(r.url for r in search_results_objects if hasattr(r, "url")))

            def safe_get_short_description(url):
                try:
                    desc = get_short_description(url)
                    return desc if desc else "Short description not available."
                except Exception as e:
                    logger.error(f"Error getting short description for {url}: {str(e)}")
                    return "Error fetching description."

            short_descriptions = Parallel(n_jobs=-1, prefer="threads")(
                delayed(safe_get_short_description)(url) for url in unique_urls
            )

            results = [
                {
                    "index": index + 1,
                    "url": url,
                    "title": unquote(url.split("/")[-1].replace("_", " ")),
                    "short_description": desc,
                }
                for index, (url, desc) in enumerate(zip(unique_urls, short_descriptions))
            ]

            response_data = {
                "status": "success",
                "message": "Select the article you want to read",
                "results": results,
                "query": query,
                "result_count": len(results),
            }
            cache.set(cache_key, response_data, CACHE_TIMEOUT)
            logger.info(f"Cached search results for query: '{query}'")
            return JsonResponse(response_data)

        except Exception as e:
            logger.error(f"Search error for query '{query}': {str(e)}", exc_info=True)
            return JsonResponse(
                {"status": "error", "message": "An error occurred while processing your search request."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class SelectLinkView(View):
    @method_decorator(validate_query_param("link", required=True, max_length=500))
    def get(self, request):
        """Handle GET request for getting available options for a Wikipedia article."""
        selected_link = request.validated_params["link"]
        logger.info(f"Options request for link: '{selected_link}' from IP: {request.META.get('REMOTE_ADDR')}")

        if not re.match(r"^https://en\.wikipedia\.org/wiki/.+$", selected_link):
            logger.warning(f"Invalid Wikipedia URL format: {selected_link}")
            return JsonResponse(
                {
                    "status": "error",
                    "message": "Invalid Wikipedia URL format. Must be a full 'https://en.wikipedia.org/wiki/...' URL.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            article_title = unquote(selected_link.split("/")[-1].replace("_", " "))
            options = [
                {"id": 1, "description": "Read short description of the page"},
                {"id": 2, "description": "Read summary of the page"},
                {"id": 3, "description": "Read the full page content"},
                {"id": 4, "description": "Read captions of images on the page"},
                {"id": 5, "description": "Read tables on the page"},
                {"id": 6, "description": "Read references and citations on the page"},
            ]
            response_data = {
                "status": "success",
                "message": "Select an option",
                "options": options,
                "article_url": selected_link,
                "article_title": article_title,
            }
            return JsonResponse(response_data)
        except Exception as e:
            logger.error(f"Error in SelectLinkView for link '{selected_link}': {str(e)}", exc_info=True)
            return JsonResponse(
                {"status": "error", "message": "An error occurred while fetching options for the article."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ProcessOptionView(View):
    @method_decorator(validate_query_param("link", required=True, max_length=500))
    @method_decorator(validate_query_param("option", required=True, max_length=1))
    def get(self, request):
        """Handle GET request for processing selected options on a Wikipedia article."""
        selected_link = request.validated_params["link"]
        option_str = request.validated_params["option"]
        logger.info(
            f"Processing option '{option_str}' for link: '{selected_link}' from IP: {request.META.get('REMOTE_ADDR')}"
        )

        if not re.match(r"^https://en\.wikipedia\.org/wiki/.+$", selected_link):
            logger.warning(f"Invalid Wikipedia URL format: {selected_link}")
            return JsonResponse(
                {
                    "status": "error",
                    "message": "Invalid Wikipedia URL format. Must be a full 'https://en.wikipedia.org/wiki/...' URL.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            option = int(option_str)
            if not (1 <= option <= 6):
                logger.warning(f"Invalid option value: {option}. Must be between 1 and 6.")
                return JsonResponse(
                    {"status": "error", "message": "Invalid option. Please select a valid option (1-6)."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except ValueError:
            logger.warning(f"Invalid option format: '{option_str}'. Must be an integer.")
            return JsonResponse(
                {"status": "error", "message": "Invalid option format. Option must be a number (1-5)."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        page_title_url_part = selected_link.split("/")[-1]
        cache_key = f"article_processing:{page_title_url_part}_option:{option}"
        cached_response = cache.get(cache_key)
        if cached_response:
            logger.info(f"Serving processed option from cache for key: {cache_key}")
            return JsonResponse(cached_response)

        try:
            content = None
            content_type = ""
            article_title = unquote(page_title_url_part.replace("_", " "))
            additional_meta = {}

            if option == 1:  # Short description
                content_type = "short_description"
                content = get_short_description(selected_link)
                content = content if content else "Short description not available."
            elif option == 2:  # Page summary
                content_type = "summary"
                summary_text = mediawiki_api.get_page_summary(page_title_url_part)
                content = re.sub(r"[\n\t\r]+", " ", summary_text).strip() if summary_text else "Summary not available."
            elif option == 3:  # Full page content
                content_type = "full_content"
                content = get_full_content(selected_link)
                content = content if content else "Full content not available."
            elif option == 4:  # Image captions
                content_type = "image_captions"
                content = fetch_and_process_images(selected_link)
                additional_meta["image_count"] = len(content) if isinstance(content, list) else 0
                content = content if content else []  # Ensure it's a list
            elif option == 5:  # Tables
                content_type = "tables"
                content = get_tables(selected_link)
                additional_meta["table_count"] = len(content) if isinstance(content, list) else 0
                content = content if content else []  # Ensure it's a list
            elif option == 6:  # References
                content_type = "citations"
                content = get_citations(selected_link)
                additional_meta["citation_count"] = len(content) if isinstance(content, list) else 0
                content = content if content else []  # Ensure it's a list

            response_data = {
                "status": "success",
                "type": content_type,
                "content": content,
                "article_url": selected_link,
                "article_title": article_title,
                **additional_meta,
            }

            cache.set(cache_key, response_data, CACHE_TIMEOUT)
            logger.info(f"Cached processed option for key: {cache_key}")
            return JsonResponse(response_data)

        except Exception as e:
            logger.error(f"Error processing option {option} for '{selected_link}': {str(e)}", exc_info=True)
            return JsonResponse(
                {
                    "status": "error",
                    "message": f"Failed to process your request for option {option}. Please try again later.",
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
