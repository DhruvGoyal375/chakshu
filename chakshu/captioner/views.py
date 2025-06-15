import base64
import re
import time
import urllib.parse
from functools import wraps
from io import BytesIO

import requests
from bs4 import BeautifulSoup
from config import IMAGE_CAPTIONING_PROMPT, MODEL_NAME
from core.logger import setup_logger
from core.utils import get_env_variable
from django.core.cache import cache
from django_ratelimit.decorators import ratelimit
from joblib import Parallel, delayed
from PIL import Image, UnidentifiedImageError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ImageCaption, WikipediaPage

# Initialize module-level logger
logger = setup_logger(__name__)

# Standard headers for requests
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}


def validate_url_param(param_name="link", required=True):
    """Decorator to validate a URL parameter in a request."""

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            url = request.data.get(param_name)
            if required and not url:
                return Response(
                    {"status": "error", "message": f"'{param_name}' is required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if url and not re.match(r"^https?://en\.wikipedia\.org/wiki/\S+$", url):
                return Response(
                    {"status": "error", "message": "Invalid Wikipedia URL format."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator


def _fetch_api(url, params=None, max_retries=3):
    """Generic function to fetch data from an API with error handling and retry logic."""
    last_exception = None
    for attempt in range(max_retries):
        try:
            response = requests.get(url, params=params, headers=HEADERS, timeout=15)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            return response.json()
        except requests.exceptions.HTTPError as e:
            last_exception = e
            if e.response.status_code == 429:
                retry_after = e.response.headers.get("Retry-After")
                if retry_after:
                    try:
                        wait_time = int(retry_after)
                        logger.warning(f"Rate limit hit. Retrying after {wait_time} seconds.")
                        time.sleep(wait_time)
                    except (ValueError, TypeError):
                        logger.warning("Invalid Retry-After header. Using exponential backoff.")
                        wait_time = 2 ** (attempt + 1)
                        time.sleep(wait_time)
                else:
                    # Exponential backoff if Retry-After is not provided
                    wait_time = 2 ** (attempt + 1)
                    logger.warning(f"Rate limit hit. Retrying in {wait_time} seconds.")
                    time.sleep(wait_time)
            else:
                # For other HTTP errors, don't retry
                logger.error(f"API request failed for {url}: {e}", exc_info=True)
                return None
        except requests.exceptions.RequestException as e:
            last_exception = e
            logger.warning(f"API request attempt {attempt + 1}/{max_retries} failed for {url}: {e}")
            time.sleep(2 ** (attempt + 1))  # Exponential backoff for other request errors

    logger.error(
        f"API request failed for {url} after {max_retries} retries. Last exception: {last_exception}", exc_info=True
    )
    return None


def fetch_page_parsed_content(page_title):
    """Fetch parsed Wikipedia page content to extract structured captions."""
    api_url = (
        f"https://en.wikipedia.org/w/api.php?action=parse&page={urllib.parse.quote(page_title)}&format=json&prop=text"
    )
    response_data = _fetch_api(api_url)
    return response_data["parse"]["text"]["*"] if response_data and "parse" in response_data else None


def extract_captions_from_figcaption(parsed_content):
    """Extract image captions from <figcaption> inside <figure> tags."""
    captions = {}
    if not parsed_content:
        return captions
    soup = BeautifulSoup(parsed_content, "html.parser")
    for figure in soup.find_all("figure"):
        img = figure.find("img")
        figcaption = figure.find("figcaption")
        link = figure.find("a")
        if img and figcaption and link:
            img_url = link.get("href", "")
            img_filename = img_url.split("/")[-1].replace("File:", "").replace("_", " ")
            if img_filename:
                captions[img_filename] = figcaption.get_text(strip=True)
    return captions


def get_high_resolution_image_url(image_title):
    """Fetch the highest resolution version of an image from a title."""
    commons_api = "https://commons.wikimedia.org/w/api.php"
    params = {
        "action": "query",
        "titles": image_title,
        "prop": "imageinfo",
        "iiprop": "url",
        "iiurlwidth": 4000,
        "format": "json",
    }
    response_data = _fetch_api(commons_api, params=params)
    if response_data:
        pages = response_data.get("query", {}).get("pages", {})
        for page in pages.values():
            if "imageinfo" in page:
                return page["imageinfo"][0]["url"]
    return None


def clean_html(raw_html):
    """Remove HTML tags using regex."""
    return re.sub(r"<[^>]*>", "", raw_html) if raw_html else ""


def fetch_image_as_base64(image_url):
    """Downloads an image, processes it, and returns a base64-encoded string."""
    try:
        response = requests.get(image_url, headers=HEADERS, stream=True, timeout=20)
        response.raise_for_status()

        image_bytes = BytesIO(response.content)
        with Image.open(image_bytes) as image:
            if image.mode == "RGBA":
                background = Image.new("RGB", image.size, (128, 128, 128))
                background.paste(image, (0, 0), image)
                image = background

            image = image.resize((512, 512), Image.LANCZOS)
            image_format = image.format or "JPEG"

            buffered = BytesIO()
            image.save(buffered, format=image_format)
            return base64.b64encode(buffered.getvalue()).decode("utf-8")

    except (OSError, requests.exceptions.RequestException, UnidentifiedImageError) as e:
        logger.warning(f"Failed to fetch or process image {image_url}: {e}")
        return None


def generate_image_caption(encoded_image, title, caption, description):
    """Generates a detailed caption for an image using a remote image captioning model."""
    if not encoded_image:
        return None

    prompt = IMAGE_CAPTIONING_PROMPT.format(Title=title, Caption=caption, Description=description)
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "images": [encoded_image],
        "stream": False,
        "options": {"temperature": 0, "top_p": 0.1, "top_k": 1},
    }

    try:
        start_time = time.time()
        ollama_url = f"{get_env_variable('OLLAMA_BASE_URL', 'http://localhost:11434')}/api/generate"
        response = requests.post(ollama_url, json=payload, timeout=60)
        response.raise_for_status()
        end_time = time.time()
        logger.info(f"Image caption generated in {end_time - start_time:.2f}s.")
        return response.json().get("response")
    except requests.exceptions.RequestException as e:
        logger.error(f"Image captioning server request failed: {e}", exc_info=True)
        return None


def _process_single_image(img_info, all_captions):
    """Process a single image: fetch data, generate caption, and return structured result."""
    img_title_raw = img_info["title"]
    img_title_clean = img_title_raw.replace("File:", "")

    high_res_url = get_high_resolution_image_url(img_title_raw)
    if not high_res_url:
        logger.warning(f"Could not find high-resolution URL for {img_title_raw}")
        return None

    encoded_image = fetch_image_as_base64(high_res_url)
    if not encoded_image:
        return None

    # Fetch metadata for caption context
    api_url = f"https://en.wikipedia.org/w/api.php?action=query&prop=imageinfo&iiprop=extmetadata&format=json&titles={urllib.parse.quote(img_title_raw)}"
    metadata_response = _fetch_api(api_url)
    metadata = {}
    if metadata_response:
        pages = metadata_response.get("query", {}).get("pages", {})
        for page in pages.values():
            if "imageinfo" in page:
                metadata = page["imageinfo"][0].get("extmetadata", {})
                break

    title_caption = clean_html(metadata.get("ImageDescription", {}).get("value"))
    description = clean_html(metadata.get("ObjectName", {}).get("value"))
    real_caption = clean_html(all_captions.get(img_title_clean, ""))

    generated_caption = generate_image_caption(encoded_image, title_caption, real_caption, description)
    if not generated_caption:
        logger.warning(f"Failed to generate image caption for {high_res_url}")
        return None

    return {"image_url": high_res_url, "final_caption": generated_caption}


def fetch_and_process_page_images(page_title, page_url):
    """Orchestrates fetching, processing, and storing image captions for a Wikipedia page."""
    page, created = WikipediaPage.objects.get_or_create(url=page_url, defaults={"title": page_title})
    if created:
        logger.info(f"Created new page entry for {page_title}")

    # 1. Fetch all image titles from the page
    api_url = f"https://en.wikipedia.org/w/api.php?action=query&prop=images&format=json&titles={page_title}"
    response = _fetch_api(api_url)
    if not response:
        msg = "Failed to fetch image list from Wikipedia."
        raise ConnectionError(msg)

    images_to_process = []
    for page_data in response.get("query", {}).get("pages", {}).values():
        images_to_process.extend(page_data.get("images", []))

    # 2. Fetch structured captions for context
    parsed_content = fetch_page_parsed_content(page_title)
    all_captions = extract_captions_from_figcaption(parsed_content)

    # 3. Process images in parallel
    logger.info(f"Processing {len(images_to_process)} images in parallel...")
    processed_results = Parallel(n_jobs=-1, backend="threading")(
        delayed(_process_single_image)(img, all_captions) for img in images_to_process
    )

    # 4. Filter out failed jobs and save successful ones
    final_captions = []
    for result in processed_results:
        if result:
            final_captions.append(result)
            ImageCaption.objects.update_or_create(
                page=page,
                image_url=result["image_url"],
                defaults={"final_caption": result["final_caption"]},
            )

    logger.info(f"Successfully processed and saved {len(final_captions)} image captions.")
    return final_captions


class CaptionGenerationView(APIView):
    """
    API view to trigger the processing of a Wikipedia page for image captions.
    Accepts a POST request with a 'link' to a Wikipedia page.
    """

    @ratelimit(key="ip", rate=get_env_variable("RATE_LIMIT", "5/m"), method="POST", block=True)
    @validate_url_param(param_name="link")
    def post(self, request, *args, **kwargs):
        page_url = request.data.get("link")
        cache_key = f"wikipedia_captions:{page_url}"
        cache_timeout = int(get_env_variable("CACHE_TIMEOUT_SECONDS", 3600))

        try:
            # 1. Check cache first
            cached_data = cache.get(cache_key)
            if cached_data:
                logger.info(f"Cache hit for {page_url}")
                return Response({"status": "success", "source": "cache", "data": cached_data})

            # 2. Check database
            page = WikipediaPage.objects.filter(url=page_url).first()
            if page:
                db_captions = list(ImageCaption.objects.filter(page=page).values("image_url", "final_caption"))
                if db_captions:
                    logger.info(f"DB hit for {page_url}")
                    cache.set(cache_key, db_captions, timeout=cache_timeout)
                    return Response({"status": "success", "source": "database", "data": db_captions})

            # 3. Process the page if not in cache or DB
            logger.info(f"Processing page: {page_url}")
            page_title = urllib.parse.unquote(page_url.split("/")[-1])
            processed_captions = fetch_and_process_page_images(page_title, page_url)

            if processed_captions:
                cache.set(cache_key, processed_captions, timeout=cache_timeout)
                return Response({"status": "success", "source": "processed", "data": processed_captions})
            else:
                return Response(
                    {"status": "error", "message": "No processable images found on the page."},
                    status=status.HTTP_404_NOT_FOUND,
                )

        except ConnectionError as e:
            logger.error(f"Network error while processing {page_url}: {e}", exc_info=True)
            return Response(
                {"status": "error", "message": "Failed to connect to external services."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        except Exception as e:
            logger.critical(f"An unexpected error occurred for {page_url}: {e}", exc_info=True)
            return Response(
                {"status": "error", "message": "An internal server error occurred."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
