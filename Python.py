#EmailHarvester.py

import re
import requests
from bs4 import BeautifulSoup
import time

def searchEmails(query):
  headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 >
  url = f'https://html.duckduckgo.com/html/?q={query}'

  try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
  except Exception as e:
    print(f'Failed to fetch search results: {e}')
    return set()

  soup = BeautifulSoup(response.text, 'html.parser')
  links = [a['href'] for a in soup.find_all('a', href=True)]
  emails = set()

  for link in links:
    if not link.startswith('http'):
        link = 'https://duckduckgo.com' + link
    try:
      page = requests.get(link, headers=headers)
      found = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', page.text)
      emails.update(found)
    except Exception as e:
      print(f'Error processing {link}: {e}')
      pass
    time.sleep(1) #Be polite to the servers!
  return emails

if __name__ == '__main__':
  print('This script is for educational use only! Do not use it to collect or contact individuals without consent!')
  target = input('Enter Search Term: ')
  results = searchEmails(target)
  if results:
    for email in results:
      print(email)
  else:
    print('No emails found')
