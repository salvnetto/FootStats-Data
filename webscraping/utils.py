import requests

from bs4 import BeautifulSoup


def getTeamsUrl(url):
  data = requests.get(url)
  soup = BeautifulSoup(data.text, features= 'lxml')
  table = soup.select('table.stats_table')[0]           
  links = table.find_all('a')                           
  links = [link.get('href') for link in links]          
  links = [link for link in links if '/squads/' in link]  
  urls = [f"https://fbref.com{link}" for link in links]
  
  return urls