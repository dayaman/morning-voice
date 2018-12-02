# coding: utf-8
import re
import requests
import json
import datetime
from bs4 import BeautifulSoup
    

def get_weath():
    # いろんな地域に対応する用
    '''
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
    '''
    city_num = '370000' #kagawa
    city_weath = requests.get('http://weather.livedoor.com/forecast/webservice/json/v1?city='+city_num)

    weath_json = city_weath.json()

    temp = maketemp(weath_json)
    now = datetime.datetime.now()
    month = datetime.datetime.strftime(now, '%-m')
    date = datetime.datetime.strftime(now, '%-d')
    hour = datetime.datetime.strftime(now, '%-H')
    minute = datetime.datetime.strftime(now, '%-M')
    msg = []
    text = ''.join(weath_json['description']['text'].splitlines()).replace(' ', '')
    # 日時の書き方が汚いのは文字コードの問題のせい
    msg.append('おはようございます。'+month+'月'+date+'日、'+hour+'時'+minute+'分です。' \
    +weath_json['title'].replace(' ', '、')+'。' \
    +weath_json["forecasts"][0]["telop"]+'。' \
    +temp\
    +re.sub(r'東北地方(.+)',"",re.sub(r'【(.{,7})】', "", text).replace('<', '').replace('>','。')) \
    +'それでは、今日も1日、頑張って行きましょう。')
    msg.append(weath_json['title'])
    return msg

def maketemp(ws_json):
    msg = ''
    if ws_json['forecasts'][0]['temperature']['max'] != None:
        msg += '最高気温は{}度。'.format(ws_json['forecasts'][0]['temperature']['max']['celsius'])

    if ws_json['forecasts'][0]['temperature']['min'] != None:
        msg += '最低気温は{}度。'.format(ws_json['forecasts'][0]['temperature']['min']['celsius'])
    return msg
