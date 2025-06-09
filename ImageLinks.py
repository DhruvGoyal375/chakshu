from bs4 import BeautifulSoup
import pandas as pd
import requests

import os
import time
class Page:
  URLS = []
  soup: BeautifulSoup
  selfURL: str
  pageName: str
  visited: bool

  #for main Url -> isMain = true
  def __init__(self,page,isMain):
    if not os.path.isdir("/content/" + page):
      self.visited = False
      os.mkdir("/content/" + page)
    else:
      #main page must always be initialized
      if not isMain:
        self.visited = True
        return
    self.selfURL = "https://en.wikipedia.org/wiki/" + page
    self.pageName = page
    pageUrl = requests.get(self.selfURL)
    if pageUrl.status_code != 200:
      return
    self.soup = BeautifulSoup(pageUrl.text,parser = 'html')
    os.chdir("/content/" + self.pageName)

  def Scrape(self):
    self.LINKS();
    self.IMAGES();


  def LINKS(self):
    AllLinks =[]
    for tag in self.soup.find_all("a"):
      try:
        AllLinks.append(tag['href'])
      except KeyError as e:
        continue
    AllLinks = sorted(AllLinks)
    slashDict = {}
    slashes = []

    for link in AllLinks:
      countSlash = link.count('/')
      if countSlash not in slashes:
         slashes.append(countSlash)
      if countSlash not in slashDict:
         slashDict[countSlash] = []
      slashDict[countSlash].append(link)
    df = pd.DataFrame({'Title':[],'Link':[]})

    with open("Links.csv",'wb') as linkFile:
      #contains # that is in page contents
      for link in slashDict[0]:
        if link.find('#') == 0:
          df.loc[len(df)] = [self.pageName + link,"https://en.wikipedia.org/wiki/" + self.pageName + link]

      for link in slashDict[2]:
        #contains external page name
          if link.find("/wiki/") == 0:
              df.loc[len(df)] = [link[6:],"https://en.wikipedia.org" + link]
              self.URLS.append(link[6:])
      df.to_csv(linkFile,sep = ',')

  def IMAGES(self):
      numbering = 1
      if not os.path.isdir("/content/" + self.pageName + "/Images"):
        os.mkdir("/content/" + self.pageName + "/Images")
      os.chdir("/content/" + self.pageName + "/Images")
      images = self.soup.find_all('img')
      for image in images:
     #if image is not of the type //upload
        if image['src'].find("upload")==-1:
            continue
     #use the word after / as file name
        imageLink = "https:" + image['src']
        imageName = f'''Image{numbering}.jpg'''
        try:
          imageFile = requests.get(imageLink,params = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0'})
        except requests.models.InvalidURL as u:
          continue
        with open(imageName,'wb') as img:
          img.write(imageFile.content)
          time.sleep(0.00001)
        numbering+=1

  def Traverse(self):
    self.Scrape()
    self.visited = True
    for link in self.URLS:
      thisPage = Page(link,False)
      if not thisPage.visited:
        thisPage.Scrape()
        print(thisPage.pageName)

mainUrl = Page("Flower",True)
mainUrl.Traverse()
