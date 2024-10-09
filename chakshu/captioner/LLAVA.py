import base64
import io
import json

import requests
from bs4 import BeautifulSoup
from PIL import Image


def download_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        return Image.open(io.BytesIO(response.content))
    else:
        msg = f"Failed to download image. Status code: {response.status_code}"
        raise Exception(msg)


def encode_image(image):
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")


def gather_image_metadata(image_url):
    """Fetch and print concise metadata for an image from Wikipedia or Wikimedia."""
    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            metadata = {}

            # Extract title
            title_tag = soup.find("h1", {"id": "firstHeading"})
            metadata["title"] = title_tag.text if title_tag else "No title"

            # Extract description (first paragraph)
            description_tag = soup.find("div", {"class": "description"})
            if description_tag:
                # Get the first paragraph for a concise description
                paragraph = description_tag.find("p")
                metadata["description"] = paragraph.text if paragraph else "No description"
            else:
                metadata["description"] = "No description"

            # Print concise metadata
            print(f"Title: {metadata['title']}")
            print(f"Description: {metadata['description']}")
        else:
            print(f"Failed to fetch metadata, status code: {response.status_code}")
    except Exception as e:
        print(f"Error fetching metadata: {str(e)}")
    return metadata


def create_prompt(metadata, prompt_template):
    """Dynamically insert metadata into the prompt template."""
    title = metadata.get("title", "No title")
    description = metadata.get("description", "No description")

    # Fill in the template
    return prompt_template.format(Title=title, Description=description)


def test_model_with_image_url_and_text(image_url, prompt_template, page_url):
    try:
        # Download the image
        image = download_image(image_url)

        # Get metadata
        metadata = gather_image_metadata(page_url)

        # Encode the image to base64
        encoded_image = encode_image(image)

        # Create the final prompt
        full_prompt = create_prompt(metadata, prompt_template)
        print("Full prompt being sent to the model:")
        print(full_prompt)

        # Define the payload
        payload = json.dumps(
            {
                "model": "llava",  # Change this to the model you're using if it's different
                "prompt": full_prompt,
                "images": [encoded_image],
                "stream": False,
            }
        )

        # Send the request to the API
        response = requests.post(
            "http://localhost:11434/api/generate", data=payload, headers={"Content-Type": "application/json"}
        )

        # Check if the request was successful
        if response.status_code == 200:
            result = response.json()
            print("Response from model:")
            print(result["response"])
        else:
            print(f"Error: Received status code {response.status_code}")
            print(response.text)

    except Exception as e:
        print(f"An error occurred: {e}")


# General prompt template for all image descriptions
prompt_template = """
Analyze and describe the content of the image based on the metadata provided. Use the following guidelines:

1. Identify and name any individuals, places, or objects mentioned in the metadata.
2. Describe their positions and actions within the scene (e.g., who is on the left, right, etc.).
3. Include any notable interactions or movements.
4. Provide a detailed overview of the image that a blind person could understand, including visual cues like colors, lighting, and emotions where possible.

Use the following metadata to guide your description:

Image Metadata:
Title: {Title}
Description: {Description}

Ensure the description incorporates the names of people or places mentioned, along with their actions and relationships in the scene suitable for a blind person . Do not include any technical details like links,metadata etc. The description should focus on helping a blind person understand the visual content.
"""


# Example usage:
page_url = "https://commons.wikimedia.org/wiki/File:Narendra_Modi_and_Prime_Minister_Atal_Bihari_Vajpayee_in_New_Delhi_in_October_12,_2001.jpg"
image_url = "https://upload.wikimedia.org/wikipedia/commons/0/0f/Narendra_Modi_and_Prime_Minister_Atal_Bihari_Vajpayee_in_New_Delhi_in_October_12%2C_2001.jpg"
test_model_with_image_url_and_text(image_url, prompt_template, page_url)
