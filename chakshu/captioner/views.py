import requests
import urllib.parse
import time  # Import the time module
import ollama
from PIL import Image, UnidentifiedImageError
from io import BytesIO
import base64
import re
from bs4 import BeautifulSoup
from config import MODEL_NAME, MODEL_URL


from django.core.cache import cache
from .models import WikipediaPage, ImageCaption

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
}


def fetch_page_parsed_content(page_title):
    """Fetch parsed Wikipedia page content to extract structured captions."""
    api_url = f"https://en.wikipedia.org/w/api.php?action=parse&page={urllib.parse.quote(page_title)}&format=json&prop=text"
    response = requests.get(api_url, headers=headers).json()

    if "parse" in response and "text" in response["parse"]:
        return response["parse"]["text"]["*"]  # Returns HTML-like content
    return None

def extract_captions_from_figcaption(parsed_content):
    """Extract image captions from <figcaption> inside <figure> tags."""
    captions = {}
    soup = BeautifulSoup(parsed_content, "html.parser")

    for figure in soup.find_all("figure"):
        img = figure.find("img")
        figcaption = figure.find("figcaption")
        link = figure.find("a")  # Get <a> tag linking to the full image

        if img and figcaption and link:
            # Extract full image filename from <a href>, removing "File:" prefix
            img_url = link.get("href", "")
            img_filename = img_url.split("/")[-1].replace("File:", "").replace("_", " ")  # Remove "File:"

            if img_filename:
                captions[img_filename] = figcaption.get_text(strip=True)  # Store caption

    return captions



def get_high_resolution_image_url(image_url):
    """Fetch the highest resolution version of an image."""
    try:
        filename = image_url.split("/")[-1]
        commons_api = "https://commons.wikimedia.org/w/api.php"
        params = {"action": "query", "titles": f"File:{filename}", "prop": "imageinfo", "iiprop": "url", "iiurlwidth": 4000, "format": "json"}
        response = requests.get(commons_api, params=params, headers=headers).json()

        pages = response.get("query", {}).get("pages", {})
        for page in pages.values():
            if "imageinfo" in page:
                return page["imageinfo"][0]["url"]
    except Exception as e:
        print(f"Error fetching high-resolution image: {e}")
    return image_url




def clean_html(raw_html):
    """Remove HTML tags using regex."""
    return re.sub(r'<[^>]*>', '', raw_html)


def fetch_image(image_url):
    """Downloads an image from a URL, processes it, and returns a base64-encoded string."""
    try:
        response = requests.get(image_url, headers=headers, stream=True)
        if response.status_code != 200:
            print(f"Failed to download image: {image_url}, status code: {response.status_code}")
            return None

        image_bytes = BytesIO(response.content)
        try:
            image = Image.open(image_bytes)

            # Handle transparency for RGBA images
            if image.mode == "RGBA":
                alpha = image.getchannel("A")
                if alpha.getextrema()[0] < 255:  # If there's transparency
                    background = Image.new("RGB", image.size, (128, 128, 128))
                    background.paste(image, (0, 0), image)
                    image = background

            # Resize for efficiency
            image = image.resize((512, 512), Image.LANCZOS)

            # Detect format (default to JPEG if unknown)
            image_format = image.format if image.format else "JPEG"

            # Convert to base64 directly without saving
            buffered = BytesIO()
            image.save(buffered, format=image_format)
            return base64.b64encode(buffered.getvalue()).decode("utf-8")

        except UnidentifiedImageError:
            print(f"UnidentifiedImageError: Cannot open {image_url}")
            return None
    except Exception as e:
        print(f"Error fetching image {image_url}: {e}")
        return None



def generate_llava_caption(encoded_image, title_caption, caption, description):
    """Generates a detailed caption for an image tailored for visually impaired individuals."""
    # Ensure valid image encoding
    if not encoded_image:
        print("Image encoding failed.")
        return None

    prompt = (
        f"Analyze and describe the content of the image based on the metadata provided. Use the following guidelines:\n\n"
        f"1. Identify and name any individuals, places, or objects mentioned in the metadata.\n"
        f"2. Describe their positions and actions within the scene (e.g., who is on the left, right, etc.).\n"
        f"3. Include any notable interactions or movements.\n"
        f"4. Provide a detailed overview of the image that a blind person could understand, including visual cues like colors, lighting, and emotions where possible.\n\n"
        f"Use the following metadata to guide your description:\n\n"
        f"Image Metadata:\n"
        f"Title: {title_caption.strip()}\n"
        f"Caption: {caption.strip()}\n"
        f"Description: {description.strip()}\n\n"
        f"Ensure the description incorporates the names of people or places mentioned, along with their actions and relationships in the scene suitable for a blind person. "
        f"Do not include any technical details like links, metadata, etc. The description should focus on helping a blind person understand the visual content.\n"
    )

    # Prepare the payload for the remote API request with system message included
    payload = {
        "model": MODEL_NAME,   # Specify the model name running on the server (e.g., "llava")
        "prompt": (
            "[System message]: Forget all previous messages. Focus only on the given image and its specific context. "
            "You are an AI generating precise, descriptive captions for visually impaired individuals, "
            "ensuring accuracy and clarity. Always prioritize accuracy over assumption.\n\n"
            "[User]: " + prompt  # Append the user message
        ),
        "images": [encoded_image],   # Send the image in base64 format
        "stream": False,             # Disable streaming to get the full response at once
        "options": {
            "temperature": 0, 
            "top_p": 0.1, 
            "top_k": 1
        }
    }


    # Send the request to the remote LLaVA server
    try:
        # Start timer
        start_time = time.time()

        response = requests.post(MODEL_URL, json=payload)

        # Stop timer
        end_time = time.time()

        # Check the response status
        if response.status_code == 200:
            result = response.json()
            print(f"Time taken to generate caption: {end_time - start_time:.2f} seconds")
            return result.get("response",{})
        else:
            print(f"Failed to generate caption. Status code: {response.status_code}")
            return None

    except Exception as e:
        print(f"Error: {e}")
        return None

def process_image(image_url, title, caption, description):
    encoded_image = fetch_image(image_url)    
    if encoded_image is None:
        print("Image processing failed.")
        return
    print(image_url, title,caption,description)
    llava_caption = generate_llava_caption(encoded_image, title, caption, description)

    print(f"Image URL: {image_url}")
    print(f"LLaVA Caption: {llava_caption}")
    print("------")
    return llava_caption
    
def fetch_and_process_images(page_url):
    """Fetch all images from a Wikipedia page along with their real captions."""
    
    # Check if captions are in cache
    cache_key = f"wikipedia:{page_url}"
    cached_captions = cache.get(cache_key)
    
    if cached_captions:
        print("Cache hit. Returning cached captions.")
        return cached_captions

    # Check if captions are in the database
    page = WikipediaPage.objects.filter(url=page_url).first()
    
    if page:
        # Fetch captions from DB
        db_captions = list(
            ImageCaption.objects.filter(page=page).values('image_url', 'final_caption')
        )
        
        if db_captions:
            print("DB hit. Returning stored captions.")
            
            # Store in cache before returning
            cache.set(cache_key, db_captions, timeout=60 * 60)  # Cache for 1 hour
            return db_captions

    # Otherwise, process the page
    print("No cache or DB hit. Fetching and processing.")
    page_title = urllib.parse.unquote(page_url.split("/")[-1])
    page, created = WikipediaPage.objects.get_or_create(
        url=page_url,
        defaults={'title': page_title}
    )
    # Fetch images and process captions
    processed_captions = []

    # Get parsed content and extract captions
    parsed_content = fetch_page_parsed_content(page_title)
    image_captions = extract_captions_from_figcaption(parsed_content) if parsed_content else {}

    # Fetch image metadata via API
    api_url = f"https://en.wikipedia.org/w/api.php?action=query&prop=images&format=json&titles={page_title}"
    continue_param = {}

    while True:
        response = requests.get(api_url, params=continue_param, headers=headers).json()
        pages = response.get("query", {}).get("pages", {})

        for page_data in pages.values():
            if "images" in page_data:
                for img in page_data["images"]:
                    img_title = img["title"].replace("File:", "")

                    # Fetch image metadata (URL, description)
                    img_url_api = f"https://en.wikipedia.org/w/api.php?action=query&prop=imageinfo&iiprop=url|extmetadata&format=json&titles={urllib.parse.quote(img['title'])}"
                    img_response = requests.get(img_url_api, headers=headers).json()

                    for img_page in img_response.get("query", {}).get("pages", {}).values():
                        if "imageinfo" in img_page:
                            for img_data in img_page["imageinfo"]:
                                img_url = img_data["url"]
                                
                                # Get high-res version
                                high_res_img_url = get_high_resolution_image_url(img_url)

                                metadata = img_data.get("extmetadata", {})

                                # Extract text captions and clean HTML tags
                                title_caption = clean_html(metadata.get("ImageDescription", {}).get("value", "")) or \
                                                clean_html(metadata.get("Caption", {}).get("value", ""))
                                description = clean_html(metadata.get("ObjectName", {}).get("value", ""))
                                real_caption = clean_html(image_captions.get(img_title, ""))

                                # Process image and generate LLaVA caption
                                llava_caption = process_image(
                                    high_res_img_url, 
                                    title_caption, 
                                    real_caption, 
                                    description
                                )

                                if llava_caption:
                                    # Store only the LLaVA caption as final_caption
                                    ImageCaption.objects.create(
                                        page=page,
                                        image_url=high_res_img_url,
                                        final_caption=llava_caption
                                    )

                                    #Add to processed captions list
                                    processed_captions.append({
                                        'image_url': high_res_img_url,
                                        'final_caption': llava_caption
                                    })

        # Handle pagination
        if "continue" in response:
            continue_param = response["continue"]
        else:
            break

    # Cache the results
    cache.set(cache_key, processed_captions, timeout=60 * 60)  # Cache for 1 hour

    return processed_captions

# # Example Wikipedia page
# wiki_url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
# fetch_and_process_images(wiki_url)
