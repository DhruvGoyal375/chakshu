from transformers import pipeline
import warnings
import ollama
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import urllib.request
warnings.filterwarnings('ignore') 

def scrape_main_images(wikipedia_url):
    response = requests.get(wikipedia_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    images = []
    base_url = "{0.scheme}://{0.netloc}".format(urlparse(wikipedia_url))

    for img_tag in soup.find_all('img'):
        parent_div = img_tag.find_parent('div', class_='infobox') or img_tag.find_parent('div', class_='thumb')
        
        img_url = urljoin(base_url, img_tag['src'])

        description = img_tag.get('alt', 'No description available')

        try:
            img_response = requests.get(img_url, stream=True)
            img_response.raise_for_status()
            img_size = int(img_response.headers.get('content-length', 0))
        except Exception as e:
            print(f"Error fetching image: {e}")
            continue

        if img_size > 20000 or parent_div:
            images.append({'description': description, 'img_url': img_url})

    return images

def download_images(images, download_folder='images'):
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    for img in images:
        img_url = img['img_url']
        img_description = img['description']
        img_name = os.path.join(download_folder, os.path.basename(img_url))
        urllib.request.urlretrieve(img_url, img_name)

wikipedia_url = 'https://en.wikipedia.org/wiki/Narendra_Modi' 
images = scrape_main_images(wikipedia_url)
download_images(images)

def generate_caption(img_path,con):
    captioner = ollama.generate(
                model="llava-llama3",
                prompt=f"{img_path} describe this image in the most detailed way with all minute details")
    caption_text = captioner['response']
    print("Caption Generated")
    caption = caption_text
    further_context = con
    output = ollama.generate(
                model="llama3.1",
                prompt=f"Generate a detailed description of the image based on the provided caption '{caption}'. Incorporate the additional context '{further_context}' to fully understand the subject matter, whether it's a person, object, or scene from a movie. Your description should be comprehensive and precise, covering all notable details in a concise manner. The final output should be between 15 to 50 words, vividly capturing the essence of the image as if you were explaining it to someone who can't see it.")
    out = output["response"]
    return out

directory = 'images'
for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    filename = filename[6:]
    print(filename)
    li = filename.split("_")
    name = " "
    for i in li:
        name = name + " " + i
    if os.path.isfile(f):
        print(generate_caption(f,name))
