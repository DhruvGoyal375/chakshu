import asyncio
import os
import shutil
import warnings

import aiohttp
import ollama
import requests
from bs4 import BeautifulSoup
from scrapper import WikipediaImageScrapper  # Include From Image Scrapper

from chakshu.config import METADATA_IMAGE_CAPTIONER_PROMPT

warnings.filterwarnings("ignore")


class MetadataImageCaptioner:
    def __init__(self, url):
        self.url = url
        self.image_folder = "images_wiki"
        self.image_data = []
        self.captions = {}

    def generate_caption(self, context, full_description):
        """Generate a caption for an image using the LLM model."""
        prompt = METADATA_IMAGE_CAPTIONER_PROMPT.format(context=context, full_description=full_description)
        response = ollama.generate(model="wizardlm2", prompt=prompt)["response"]
        return response

    def gather_image_metadata(self, filename):
        """Gather metadata about an image from Wikimedia or Wikipedia."""
        for base_url in ["https://commons.wikimedia.org/wiki/File:", "https://en.wikipedia.org/wiki/File:"]:
            try:
                response = requests.get(base_url + filename)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, "html.parser")
                    return soup.get_text(separator="\n", strip=True).lower()
            except Exception:
                pass
        return ""

    async def process_images(self, show=False):
        async with aiohttp.ClientSession() as session:
            html_content = await scrapper.fetch_content(session, self.url)
            if not html_content:
                return {}
            image_info = scrapper.get_all_images(html_content)

            self.image_data = [img for img in image_info if scrapper.is_image_link(img["link"])]

            image_urls = ["https://" + img["link"] for img in self.image_data]
            os.makedirs(self.image_folder, exist_ok=True)

            tasks = [scrapper.download_image(session, url) for url in image_urls]
            download_results = await asyncio.gather(*tasks)

            print("Downloaded..")

            for file_path, url in download_results:
                print("LLM making Responses...")
                if file_path:
                    filename = os.path.basename(file_path)
                    full_info = scrapper.gather_image_metadata(filename)
                    clean_name = scrapper.clean_filename(filename)
                    description = next(
                        (img["description"] for img in self.image_data if "https://" + img["link"] == url),
                        "Description not found.",
                    )
                    caption = self.generate_caption(f"{clean_name} {description}", full_description=full_info)
                    if show:
                        print(filename, ":", caption)
                    self.captions[url] = caption

            shutil.rmtree(self.image_folder, ignore_errors=True)
            return self.captions

    async def process_single_image(self, image_url):
        """Process a single image URL asynchronously and return a dictionary with the image URL as the key and the generated caption as the value."""
        async with aiohttp.ClientSession() as session:
            os.makedirs(self.image_folder, exist_ok=True)
            file_path, url = await scrapper.download_image(session, image_url)
            if not file_path:
                return {}

            filename = os.path.basename(file_path)
            full_info = scrapper.gather_image_metadata(filename)
            clean_name = scrapper.clean_filename(filename)
            context = clean_name
            description = "Description not found."
            caption = self.generate_caption(context, full_description=full_info)
            self.captions[url] = caption

            shutil.rmtree(self.image_folder, ignore_errors=True)
            return self.captions


if __name__ == "__main__":
    path = "https://en.wikipedia.org/wiki/James_Bond"
    scrapper = WikipediaImageScrapper(path)
    cap = MetadataImageCaptioner(path)
    single_image_caption = asyncio.run(
        cap.process_single_image("https://upload.wikimedia.org/wikipedia/commons/c/c3/Hoagy_Carmichael_-_1947.jpg")
    )
    print(single_image_caption)
