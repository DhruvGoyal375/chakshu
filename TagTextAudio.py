import re
import time
import requests
from bs4 import BeautifulSoup
from gtts import gTTS
import os

def ReadPara(para, Heading):
  paragraph = para.text
  #highlight links
  links = []
  for link in para.find_all('a'):
    #format links for different pronunciation
    paragraph = paragraph.replace(link.text, "[" + link.text + "]")
    links.append(link.text)
  audiosegments = []
  with open(Heading + ".mp3", "ab") as f:
    for word in re.split(r'[\[\]]', paragraph):
      if word.startswith(".") or word.startswith(","):
        word = word[1:]
      word.strip()
      if not word:
        continue
      try:
        if word in links:
          #remove with full stop
          links.remove(word)

          #if word contained full stop remove it.. remove it without it as well
          if word[-1] == ".":
            word = word[:-1]
          #highlight the word only once
          if word in links:
            links.remove(word)
          textSpeech = gTTS(word, lang='en', tld="co.in", slow=False)
        else:
          textSpeech = gTTS(word.strip(), lang='en', tld = "co.in", slow=False)       
        textSpeech.write_to_fp(f) 
      except AssertionError as ae:
        continue  

    
webPage = requests.get("https://en.wikipedia.org/wiki/flower")
soup = BeautifulSoup(webPage.text, features="html.parser")
text = soup.find('ul', class_="vector-toc-contents")
#show contents
textString = "Contents\n"
for tag in text.findAll("span", class_=""):
  if tag.text.find("Toggle") != -1:
    continue
  textString += tag.text + "\n"
textSpeech = gTTS(textString, lang='en',tld = 'co.in', slow=False)
os.chdir(os.getcwd())
textSpeech.save("Contents.mp3")

#show paragraph
h1 = soup.find('h1')
#show roles first
listOFPARAS = []
content = soup.find('div', id='mw-content-text')
ReadPara(h1, "Flower")
heading = "Flower"
listOFPARAS.append(heading)
os.chdir("/content/Audio")

for p in content.find_all(['p', 'h2', 'h3', 'h4', 'ul', 'li']):
  if p.name in ['h2', 'h3']:
    heading = p.text.strip()
    listOFPARAS.append(heading)
  ReadPara(p, heading)
  time.sleep(0.85)
