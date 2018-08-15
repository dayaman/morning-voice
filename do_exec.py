import subprocess
import shlex
import weath
import wave

wea_msg = weath.get_weath()
len_msg = len(wea_msg)

if len_msg > 250: #メッセージが長い時用に分割
    arr_msg = wea_msg.split('。')
    arr_len = len(arr_msg)
    #0-6 6-ｹﾂ
    arr_bef = ''
ori_args = 'python yukari.py --text '+wea_msg
cus_ori_args = shlex.split(ori_args)
doing = subprocess.run(cus_ori_args)