import requests
import sys
import pandas as pd
import argparse
from urllib.parse import urlparse
from bs4 import BeautifulSoup
# Consider using pynput for key pressed instead
def main():
   while True:
      commands: str = "S:Scrape, E:Exit"
      print("Midas's Spicy Web Scraper".center(20))
      print(commands)
      choice: str = input().lower()
      if choice == "s":
         scrapeCommands()
      if choice == "e":
         sys.exit(0)
def fetchWebsiteContent(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
         print("Error occurred. Status Code:", response.status_code)
         print("Response Body:", response.text)
         print("Response Headers:", response.headers)
    except requests.ConnectionError:
       print("Error occurred. Connection Error")
    except requests.Timeout:
       print("Request timed out")
    except requests.RequestException as e:
       print ("error occurred :", e)
def isValidUrl(url):
   parsed = urlparse(url)
   return bool(parsed.netloc) and bool(parsed.scheme)
   
def scrapeCommands():
   while True:
       localCommands: str = "E:Exit, R:Return"
       print(localCommands)
       print("Please insert a url")
       url = input()
       if url.lower() == "e":
          sys.exit(0)
       if url.lower() == "r":
          return
       if isValidUrl(url) is False:
           print("Please enter a valid url")
       else:
            WebsiteContent: str = fetchWebsiteContent(url)
            soup = BeautifulSoup(WebsiteContent, 'html.parser')
            articles = soup.find_all('article')
            articlesdata = []
            for article in articles:
               
               articleDict = {}
               for child in article.children:
                  if child.name is not None:
                     print(child)
                     if child.name in ["h1","h2","h3"]:
                        articleDict["title"] = child.get_text().strip()
                     if 'class' in child.attrs and  any(c.lower() in child['class'] for c in ['star-rating','one','two','three','four','five']):
                        print(child.attrs)
                        articleDict['rating'] = child.attrs['class'][1]
                        #that was lazy find a more generic way to do this.
                    # if 'class' in child and any(c.lower() in child['class'] for c in ['availability']):
                     #   articleDict['availability'] = child.descendants.attrs['class']
               articleDict['availability'] = article.find(class_='availability').attrs['class'][0]
                        


               #price = article.find(find_currency_symbols)
               #articleDict["price"] = price.get_text().strip()
               articleDict["price"] = article.find(string=find_currency_string)
               articlesdata.append(articleDict)
            for dictArticle in articlesdata:
               print(dictArticle)
            data = [li.get_text().strip() for li in soup.find_all('article')]
            print(data[0])
         
            df = pd.DataFrame(data)
            print(df)
            for column in df.columns:
               print(column)
            print(sys.stdout.encoding)
            break
    
def find_currency_symbols(tag):
    currency_symbols = ['$', '€', '£', '¥', '₹', '₩', '₽', '₺', '฿', '₫', '₲', '₴', '₵', '₸', '₼', '₿']
    for symbol in currency_symbols:
        if symbol in tag.get_text():
           return True
    return False
def find_currency_in_descendants(tag):
   
      for descendant in tag:
         if find_currency_symbols(descendant):
           if descendant.string:
               return descendant.string
def find_currency_string(string):
   if find_currency_symbols(string):
      return string
main()
