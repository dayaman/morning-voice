import requests
import json
from bs4 import BeautifulSoup

jp_prefs = requests.get('http://weather.livedoor.com/forecast/rss/primary_area.xml').text

soup = BeautifulSoup(jp_prefs, "html.parser")

prefs = soup.find_all('pref')

for pref in prefs:
    print(pref['title'])
    cities = pref.find_all('city')
    for city in cities:
        print('  '+city['title']+' '+city['id'])
