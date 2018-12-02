# coding: utf-8
# ソースはこちらから引用 http://blog.cgfm.jp/garyu/archives/3396
import os
import sys
import datetime
import argparse
import subprocess
import requests
import pprint
import key
 

#Docomo 音声合成 API
API_KEY = key.API_key.key
url = "https://api.apigw.smt.docomo.ne.jp/aiTalk/v1/textToSpeech?APIKEY="+API_KEY
 
def knockAPI(makemsg, msger, whr):

    # パラメーター受取
    # ===========================================

    #バイナリデータの一時保存場所
    tmp = "./cache/{}/".format(whr)
    #なければ作る
    if not os.path.isdir(tmp):
        os.makedirs(tmp)

    # wavデータの保存場所
    soundDir = "./sound/{}/".format(whr)
    # なければ作る
    if not os.path.isdir(soundDir):
        os.makedirs(soundDir)

    prm = {
        'speaker' : msger,
        'pitch' : '1.2',
        'range' : '1.2',
        'rate' : '1',
        'volume' : '2'
    }

    text = makemsg

    #現在日時を取得
    now = datetime.datetime.now()
    tstr = datetime.datetime.strftime(now, '%Y%m%d-%H%M%S')
    
    # SSML生成
    # ===========================================
    xml = u'<?xml version="1.0" encoding="utf-8" ?>'
    voice = '<voice name="' + prm["speaker"] + '">'
    prosody = '<prosody rate="'+ prm['rate'] +'" pitch="'+ prm['pitch'] +'" range="'+ prm['range'] +'">'
    xml += '<speak version="1.1">'+ voice + prosody + text + '</prosody></voice></speak>'
    
    # utf-8にエンコード
    xml = xml.encode("UTF-8")
    
    
    # Docomo APIアクセス
    # ===========================================
    print("Start API")
    
    response = requests.post(
        url,
        data=xml,
        headers={
            'Content-Type': 'application/ssml+xml',
            'Accept' : 'audio/L16',
            'Content-Length' : str(len(xml))
        }
    )
    
    #print(response)
    #print(response.encoding)
    #print(response.status_code)
    #print(response.content)
    
    if response.status_code != 200 :
        print("Error API : " + str(response.status_code))
        exit()
    
    else :
        print("Success API")
    
    #保存するファイル名
    rawFile = tstr + ".raw"
    wavFile = "voice.wav"
    
    #バイナリデータを保存
    fp = open(tmp + rawFile, 'wb')
    fp.write(response.content)
    fp.close()

    '''
    testfile = open("./sound/test.txt", "w")
    testfile.write(makemsg)
    testfile.close()
    '''
    #print("Save Binary Data : " + tmp + rawFile)
    
    
    # バイナリデータ → wav に変換
    # ===========================================
    
    # macのsoxを使って raw→wavに変換
    cmd = "sox -t raw -r 16k -e signed -b 16 -B -c 1 -v 4 " + tmp + rawFile + " "+ soundDir + wavFile
    # コマンドの実行
    subprocess.check_output(cmd, shell=True)
    
    #print("Done : " +soundDir + wavFile)
