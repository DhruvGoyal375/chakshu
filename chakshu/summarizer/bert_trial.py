from urllib.request import urlopen
from summarizer import Summarizer
import requests
from bs4 import BeautifulSoup
import urllib.parse
import time

# Start the timer
start_time = time.time()

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

url = 'https://en.wikipedia.org/wiki/James_Bond'

response = requests.get(url, headers=headers)
content = response.content

soup = BeautifulSoup(content, 'html.parser')

# Extract text from all <p> tags and store in input_text variable
paragraphs = soup.find_all('p')
scraped_text = "\n".join(para.get_text() for para in paragraphs)

print(len(scraped_text))
model = Summarizer()
text = scraped_text
summary = model(text, num_sentences=4) 
print(len(summary))
print(summary)

# End the timer and print the execution time
end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")