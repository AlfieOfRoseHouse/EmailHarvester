#EmailHarvester.py

import re
import requests
from bs4 import BeautifulSoup

def searchEmails(query):
  headers = {'User-Agent': 'Mozilla/5.0'}
  url = f'https://html.duckduckgo.com/html/?q={query}'
  response = requests.get(url, headers=headers)
  soup = BeautifulSoup(response.text, 'html.parser')
  
  links = [a['href'] for a in soup.find_all('a', href=True)]
  emails = set()
  for link in links:
    try:
      page = requests.get(link, headers=headers)
      found = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-z0-9.-]+\.[a-z]{2,}', page.text)
      emails.update(found)
    except:
      pass
  return emails

if __name__ == '__main__':
  target = input('Enter Search Term: ')
  results = searchEmails(target)
  for email in results:
    print(email)
