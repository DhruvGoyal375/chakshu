import os
import re
import urllib
import warnings

import requests
from bs4 import BeautifulSoup

warnings.filterwarnings("ignore")


class WikipediaImageScrapper:
    def __init__(self, url):
        self.url = url
        self.image_folder = "images_wiki"
        self.image_data = []

    def clean_filename(self, filename):
        name_without_extension = filename.rsplit(".", 1)[0]
        name_with_spaces = name_without_extension.replace("_", " ")
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

    def fetch_and_Save(url, path):
        r = requests.get(url)
        with open(path, "w") as f:
            f.truncate(0)
            f.write(r.text)
        print("\n File Saved \n")
        with open(path) as f:
            html_doc = f.read()
        soup = BeautifulSoup(html_doc, "html.parser")
        return soup

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

    def get_all_images(self, html_content):
        soup = BeautifulSoup(html_content, "html.parser")
        (image_info_list,) = []

        body_content = soup.find("div", id="bodyContent")
        for figure in body_content.find_all("figure"):
            image_info = self.extract_image_info("https://en.wikipedia.org" + figure.find("a")["href"])
            if image_info:
                image_info_list.append(image_info)
            figure.decompose()

        return image_info_list

    def extract_image_info(self, url):
        response = requests.get(url)
        if response.status_code != 200:
            return None

        image_page = BeautifulSoup(response.text, "html.parser")
        img_div = image_page.find("div", class_="fullImageLink", id="file")
        if img_div and img_div.find("a").has_attr("href"):
            image_link = img_div.find("a")["href"][2:]
            description = {}
            basicDescription = " ".join(
                desc.get_text(separator=" ") for desc in image_page.findAll("td", class_="description")
            )
            description["basicDescription"] = basicDescription
            imgDescription = " ".join(
                desc.get_text(separator=" ") for desc in image_page.findAll("p", class_="mw-mmv-image-desc")
            )
            description["imgDescription"] = imgDescription
            title = "".join(desc.get_text(separator=" ") for desc in image_page.findAll("span", class_="mw-mmv-title"))
            description["title"] = title
            metadata = "".join(
                desc.get_text(separator=" ") for desc in image_page.findAll("div", class_="mw-mmv-image-metadata")
            )
            description["metadata"] = metadata
            return {"link": image_link, "description": description}
        return None

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
