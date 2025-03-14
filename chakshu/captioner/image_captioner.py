import base64
import io
import json

import requests
from bs4 import BeautifulSoup
from PIL import Image

# from chakshu.config import LLAVA_IMAGE_CAPTIONER_PROMPT, MODEL_NAME, MODEL_URL
# Captioner
MODEL_URL = "http://localhost:11434/api/generate"

MODEL_NAME = "llava"

LLAVA_IMAGE_CAPTIONER_PROMPT = """
Analyze and describe the content of the image based on the metadata provided. Use the following guidelines:

1. Identify and name any individuals, places, or objects mentioned in the metadata.
2. Describe their positions and actions within the scene (e.g., who is on the left, right, etc.).
3. Include any notable interactions or movements.
4. Provide a detailed overview of the image that a blind person could understand, including visual cues like colors, lighting, and emotions where possible.

Use the following metadata to guide your description:

Image Metadata:
Title: {Title}
Description: {Description}

Ensure the description incorporates the names of people or places mentioned, along with their actions and relationships in the scene suitable for a blind person. Do not include any technical details like links, metadata, etc. The description should focus on helping a blind person understand the visual content.
"""


class LlavaImageCaptioner:
    @staticmethod
    def download_image(url):
        """Downloads an image from a URL and returns a PIL Image object."""
        response = requests.get(url)
        if response.status_code == 200:
            return Image.open(io.BytesIO(response.content))
        else:
            msg = f"Failed to download image. Status code: {response.status_code}"
            raise Exception(msg)

    @staticmethod
    def encode_image(image):
        """Encodes a PIL Image object to base64."""
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode("utf-8")

    @staticmethod
    def gather_image_metadata(image_url):
        """Fetches and returns metadata for an image from a Wikipedia/Wikimedia URL."""
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
                    paragraph = description_tag.find("p")
                    metadata["description"] = paragraph.text if paragraph else "No description"
                else:
                    metadata["description"] = "No description"

                print(f"Title: {metadata['title']}")
                print(f"Description: {metadata['description']}")
            else:
                print(f"Failed to fetch metadata, status code: {response.status_code}")
                metadata = {"title": "No title", "description": "No description"}

        except Exception as e:
            print(f"Error fetching metadata: {str(e)}")
            metadata = {"title": "No title", "description": "No description"}

        return metadata

    @staticmethod
    def create_prompt(metadata, prompt_template):
        """Dynamically inserts metadata into the provided prompt template."""
        title = metadata.get("title", "No title")
        description = metadata.get("description", "No description")
        return prompt_template.format(Title=title, Description=description)

    @classmethod
    def test_model_with_image_url_and_text(cls, image_url, prompt_template, page_url):
        """Tests the model by sending an image and prompt to the API."""
        try:
            # Download the image
            image = cls.download_image(image_url)

            # Get metadata
            metadata = cls.gather_image_metadata(page_url)

            # Encode the image to base64
            encoded_image = cls.encode_image(image)

            # Create the final prompt
            full_prompt = cls.create_prompt(metadata, prompt_template)
            print("Full prompt being sent to the model:")
            print(full_prompt)

            # Define the payload
            payload = json.dumps(
                {
                    "model": MODEL_NAME,  # Specify the model here
                    "prompt": full_prompt,
                    "images": [encoded_image],
                    "stream": False,
                }
            )

            # Send the request to the model API
            response = requests.post(MODEL_URL, data=payload, headers={"Content-Type": "application/json"})

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


# Example usage:
if __name__ == "__main__":
    # URL of the image and the page from which metadata is extracted
    page_url = "https://commons.wikimedia.org/wiki/File:Narendra_Modi_and_Prime_Minister_Atal_Bihari_Vajpayee_in_New_Delhi_in_October_12,_2001.jpg"
    image_url = "https://upload.wikimedia.org/wikipedia/commons/0/0f/Narendra_Modi_and_Prime_Minister_Atal_Bihari_Vajpayee_in_New_Delhi_in_October_12%2C_2001.jpg"

    analyzer = LlavaImageCaptioner()

    analyzer.test_model_with_image_url_and_text(image_url, LLAVA_IMAGE_CAPTIONER_PROMPT, page_url)
