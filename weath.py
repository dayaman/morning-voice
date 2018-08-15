import requests
import json
from bs4 import BeautifulSoup
    

def get_weath():
    
    ken=input('住んでいる都道府県を入力(例:東京都):')
    jp_prefs = requests.get('http://weather.livedoor.com/forecast/rss/primary_area.xml').text

    soup = BeautifulSoup(jp_prefs, "html.parser")

    pref = soup.find('pref', title=ken)

    cities = pref.find_all('city')
    i = 1
    for city in cities:
        print('{}:'.format(i) + city['title'])
        i+=1
    live_city=int(input('もっとも住んでいるのが近い街を番号で入力(半角数字):'))

    city_num = cities[live_city-1]['id']
    
    #city_num = '370000'
    city_weath = requests.get('http://weather.livedoor.com/forecast/webservice/json/v1?city='+city_num)

    weath_json = city_weath.json()

    temp = maketemp(weath_json)

    msg = weath_json['title'].replace(' ', '、')+'。' \
    +weath_json["forecasts"][0]["telop"]+'。' \
    +temp\
    +''.join(weath_json['description']['text'].splitlines()).replace(' ', '')\
    +'それでは、今日も1日、頑張って行きましょう。'

    return msg

def maketemp(ws_json):
    msg = ''
    if ws_json['forecasts'][0]['temperature']['max'] != None:
        msg += '最高気温は{}度。'.format(ws_json['forecasts'][0]['temperature']['max']['celsius'])

    if ws_json['forecasts'][0]['temperature']['min'] != None:
        msg += '最低気温は{}度。'.format(ws_json['forecasts'][0]['temperature']['min']['celsius'])
    return msg

#print(get_weath())