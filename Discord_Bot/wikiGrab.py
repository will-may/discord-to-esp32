import requests
from bs4 import BeautifulSoup

class wikiGrabber:
  def __init__(self):
        self.headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.3'}

  def search_wiki(self):
     response = requests.get("https://commons.wikimedia.org/wiki/Special:Random/File", headers = self.headers)
     content = response.content
     soup = BeautifulSoup(content, 'html.parser')
     img = soup.find_all("a", attrs={"class": "internal"})
     images = set()
     img_link = ''
     for i in img:
      img_link = i.get('href')
      images.add(img_link)
     if (not img_link == ''):
       return images
     return ''

    