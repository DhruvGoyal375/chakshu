import warnings
import os
import aiohttp
import asyncio
from bs4 import BeautifulSoup
import re
import urllib
import shutil
import ollama
import requests

warnings.filterwarnings("ignore")

class WikipediaImageCaptioner:
    def __init__(self, url):
        self.url = url
        self.image_folder = "images_wiki"
        self.image_data = []
        self.captions = {}

    def clean_filename(self, filename):
        name_without_extension = filename.rsplit('.', 1)[0]
        name_with_spaces = name_without_extension.replace('_', ' ')
        decoded_name = urllib.parse.unquote(name_with_spaces)
        return decoded_name.title()

    def is_image_link(self, url):
        """Check if a URL is an image link."""
        return re.search(r"\.(jpg|jpeg|png)$", url, re.IGNORECASE) is not None

    async def fetch_content(self, session, url):
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                return await response.text()
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None

    async def download_image(self, session, url):
        file_name = url.split("/")[-1]
        file_path = os.path.join(self.image_folder, file_name)
        try:
            async with session.get(url) as response:
                response.raise_for_status()
                with open(file_path, "wb") as file:
                    file.write(await response.read())
            return file_path, url
        except Exception as e:
            print(f"Failed to download {url}: {e}")
            return None, url
    def parse_wikipedia_page(self, html_content):
        soup = BeautifulSoup(html_content, "html.parser")
        references, image_info_list, links, main_content = [], [], [], []

        for sup in soup.find_all("sup", class_="reference"):
            a_tag = sup.find("a")
            if a_tag and a_tag.text and a_tag.has_attr("href"):
                references.append({a_tag.text: a_tag["href"]})
            sup.decompose()

        body_content = soup.find("div", id="bodyContent")
        for figure in body_content.find_all("figure"):
            image_info = self.extract_image_info("https://en.wikipedia.org" + figure.find("a")["href"])
            if image_info:
                image_info_list.append(image_info)
            figure.decompose()

        for anchor in body_content.find_all("a"):
            if anchor.has_attr("href") and anchor.text:
                link_address = anchor["href"]
                if link_address.startswith("/wiki"):
                    link_address = "https://en.wikipedia.org" + link_address
                links.append({anchor.get_text(separator=" "): link_address})

        for item in body_content.find_all(["p", "h1", "h2", "h3", "h4", "h5", "h6"]):
            content_item = {"heading": item.get_text(separator=" ")} if item.name != "p" else {"paragraph": item.get_text(separator=" ")}
            main_content.append(content_item)

        return {"references": references, "image_info": image_info_list, "links": links, "content": main_content}

    def extract_image_info(self, url):
        response = requests.get(url)
        if response.status_code != 200:
            return None

        image_page = BeautifulSoup(response.text, "html.parser")
        img_div = image_page.find("div", class_="fullImageLink", id="file")
        if img_div and img_div.find("a").has_attr("href"):
            image_link = img_div.find("a")["href"][2:]
            description = " ".join(desc.get_text(separator=" ") for desc in image_page.findAll("td", class_="description"))
            return {"link": image_link, "description": description}
        return None
    def generate_caption(self, context, full_description):
        """Generate a caption for an image using the LLM model."""
        prompt = (
            f"Create an image description that incorporates the context provided in {context}. "
            f"If the context is brief, use {full_description} to provide a more complete description of what is happening in the image. "
            "Write a clear, concise description of 30-40 words that communicates the key details about the image. "
            "The description should be in simple, easy-to-understand English, suitable for someone who cannot see the image. "
            "Focus strictly on what is visible and happening in the image, without mentioning any technical details such as image quality, resolution, or licensing."
        )
        response = ollama.generate(model="wizardlm2", prompt=prompt)["response"]
        return response

    def gather_image_metadata(self, filename):
        """Gather metadata about an image from Wikimedia or Wikipedia."""
        for base_url in ["https://commons.wikimedia.org/wiki/File:", "https://en.wikipedia.org/wiki/File:"]:
            try:
                response = requests.get(base_url + filename)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    return soup.get_text(separator='\n', strip=True).lower()
            except Exception:
                pass
        return ""

    async def process_images(self, show=False):
        async with aiohttp.ClientSession() as session:
            html_content = await self.fetch_content(session, self.url)
            if not html_content:
                return {}

            page_data = self.parse_wikipedia_page(html_content)
            self.image_data = [img for img in page_data["image_info"] if self.is_image_link(img['link'])]

            image_urls = ["https://" + img["link"] for img in self.image_data]
            os.makedirs(self.image_folder, exist_ok=True)

            # Use asynchronous downloading for images
            tasks = [self.download_image(session, url) for url in image_urls]
            download_results = await asyncio.gather(*tasks)

            print("Downloaded..")

            for file_path, url in download_results:
                print("LLM making Responses...")
                if file_path:
                    filename = os.path.basename(file_path)
                    full_info = self.gather_image_metadata(filename)
                    clean_name = self.clean_filename(filename)
                    description = next((img['description'] for img in self.image_data if "https://" + img["link"] == url), "Description not found.")
                    caption = self.generate_caption(f"{clean_name} {description}", full_description=full_info)
                    if show:
                        print(filename, ':', caption)
                    self.captions[url] = caption

            shutil.rmtree(self.image_folder, ignore_errors=True)
            return self.captions

    async def process_single_image(self, image_url):
        """Process a single image URL asynchronously and return a dictionary with the image URL as the key and the generated caption as the value."""
        async with aiohttp.ClientSession() as session:
            os.makedirs(self.image_folder, exist_ok=True)
            file_path, url = await self.download_image(session, image_url)
            if not file_path:
                return {}

            filename = os.path.basename(file_path)
            full_info = self.gather_image_metadata(filename)
            clean_name = self.clean_filename(filename)
            context = clean_name
            description = "Description not found."
            caption = self.generate_caption(context, full_description=full_info)
            self.captions[url] = caption

            shutil.rmtree(self.image_folder, ignore_errors=True)
            return self.captions


if __name__ == "__main__":
    scraper = WikipediaImageCaptioner("https://en.wikipedia.org/wiki/Narendra_Modi")
    single_image_caption = asyncio.run(scraper.process_single_image('https://upload.wikimedia.org/wikipedia/commons/0/0f/Narendra_Modi_and_Prime_Minister_Atal_Bihari_Vajpayee_in_New_Delhi_in_October_12%2C_2001.jpg'))
    print(single_image_caption)

