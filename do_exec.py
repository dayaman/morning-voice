# coding: utf-8
import datetime
import subprocess
import weath
from pydub import AudioSegment
from yukari import knockAPI

firth_msg = weath.get_weath()

wea_msg = firth_msg
len_msg = len(wea_msg)

msger = 'sumire'

if len_msg > 250: #メッセージが長い時用に分割
    arr_msg = wea_msg.split('。')
    arr_len = len(arr_msg)
    #0-6 6-ｹﾂ
    arr_bef = '。'.join(arr_msg[0:6])+'。'
    knockAPI(arr_bef, msger, "cut1")
    arr_aft = '。'.join(arr_msg[6:arr_len-1])
    knockAPI(arr_aft, msger, "cut2")
    marge = 'sox ./sound/{}/voice.wav ./sound/{}/voice.wav ./sound/{}/voice.wav'.format("cut1", 'cut2', 'nomal')
    subprocess.check_output(marge, shell=True)
else:
    knockAPI(wea_msg, msger, "nomal")

sound = AudioSegment.from_file("./sound/nomal/voice.wav", "wav")
sound_time = int(sound.duration_seconds)
# cmd = 'play ./sound/{}/voice.wav'.format("nomal")
# subprocess.check_output(cmd, shell=True)

long_cmd="""
sox ./music/am_lov.wav ./music/second.wav trim 0 {} && \
sox -n -r 16000 ./music/air.wav trim 0 {} && \
sox ./music/lovers.wav ./music/aft.wav trim {} fade 3 && \
sox ./music/air.wav ./music/aft.wav ./music/third_ch.wav && \
sox ./music/third_ch.wav ./music/third.wav fade 0 90 3 && \
sox ./sound/voiceAir.wav ./sound/nomal/voice.wav ./sound/comp_voice.wav && \
play -m ./music/fadou.wav ./music/second.wav ./music/third.wav ./sound/comp_voice.wav \
""".format(35+sound_time, 32+sound_time, 32+sound_time)
subprocess.check_output(long_cmd, shell=True)