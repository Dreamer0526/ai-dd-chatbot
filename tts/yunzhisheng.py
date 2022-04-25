# coding:utf-8
import websocket
import hashlib
import json
import time
import ssl
import base64
from functools import partial

try:
    import thread
except ImportError:
    import _thread as thread
import logging
import os
import re

logger = logging.getLogger("output")


class Ws_parms(object):
    '''
    参数类，websocket测试需要的参数相关
    '''

    def __init__(self, url, appkey, secret, pid, vcn, text, user_id, tts_format, tts_sample):
        self.url = url
        self.appkey = appkey
        self.secret = secret
        self.user_id = user_id

        self.tts_format = tts_format
        self.tts_sample = tts_sample
        self.tts_text = text
        self.tts_vcn = vcn
        self.tts_speed = 50
        self.tts_volume = 50
        self.tts_pitch = 50
        self.tts_bright = 50
        self.tts_stream = b''
        self.punc = ''
        self.status = False
        self.message = ''
        self.code = 0
        self._pid = pid

        self.logger = logging.getLogger("RunLog")

        # 指定logger输出格式
        formatter = logging.Formatter('%(asctime)s %(levelname)-8s: %(message)s')

        # 文件日志
        file_handler = logging.FileHandler("logs/log_%s" % self._pid)
        file_handler.setFormatter(formatter)  # 可以通过setFormatter指定输出格式

        # 为logger添加的日志处理器
        self.logger.addHandler(file_handler)
        # self.logger.addHandler(console_handler)

        # 指定日志的最低输出级别，默认为WARN级别
        self.logger.setLevel(logging.INFO)
        pass

    def get_sha256(self, timestamp):
        hs = hashlib.sha256()
        hs.update((self.appkey + timestamp + self.secret).encode('utf-8'))
        signature = hs.hexdigest().upper()
        return signature

    def get_url(self):
        timestamp = str(int(time.time() * 1000))
        self.url = self.url + '?' + 'time=' + timestamp + '&appkey=' + \
                   self.appkey + '&sign=' + self.get_sha256(timestamp)
        return self.url


def on_message(ws, data, wsParms):
    if type(data) is str:
        print('rec text msg:', data)
    if type(data) is bytes:
        wsParms.tts_stream += data
    print('rec byte msg:', len(data))


def on_error(ws, error):
    print("error: ", error)


def on_close():
    print("### closed ###")


def on_open(ws, wsParms):
    print('open!')

    def run(*args):
        d = {
            "format": wsParms.tts_format,
            "sample": wsParms.tts_sample,
            "text": wsParms.tts_text,
            "vcn": wsParms.tts_vcn,
            "user_id": wsParms.user_id,
            "speed": wsParms.tts_speed,
            "volume": wsParms.tts_volume,
            "pitch": wsParms.tts_pitch,
            "bright": wsParms.tts_bright,
        }
        print("data:", d)
        ws.send(json.dumps(d))
        print("my send:", wsParms.tts_vcn, wsParms.tts_format, wsParms.tts_text)

    thread.start_new_thread(run, ())


def ensure_dir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def rm_logs(dir_path):
    log_file = os.listdir(dir_path)
    for logf in log_file:
        if os.path.exists(dir_path + logf) and logf != "log.output":
            os.remove(dir_path + logf)


def do_ws(wsP):
    ws_url = wsP.get_url()
    websocket.enableTrace(False)
    print(ws_url)
    ws = websocket.WebSocketApp(url=ws_url,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = partial(on_open, wsParms=wsP)
    ws.on_message = partial(on_message, wsParms=wsP)
    ws.run_forever()
    if wsP.code == 0:
        pass
    else:
        pass
    return wsP


def write_results(wsParms):
    ensure_dir('results')
    t1 = str(int(time.time()))
    tts_stream = os.path.join('results/', t1 + '.' + wsParms.tts_format)
    with open(tts_stream, 'wb') as f:
        f.write(wsParms.tts_stream)


appkey = 'ta66z4jjxre6oogtvc3fi5c6wfmf5aniisywnkyc'
secret = 'ad6d2390c683f2dcc158c1927a09f9c6'
ws_url = 'wss://ws-stts.hivoice.cn/v1/tts'
user_id = 'unisound-python-demo'
vcn = 'xuanxuan-plus'
text = '听众朋友们，大家好。今天是2015年4月23日，星期四。欢迎大家收听今天的《天气预报》。现在为您播报今天早上6点钟发布的鄂尔多斯天气预报。今天夜间到明天白天，晴转多云，西风一到二级，最高温度25摄氏度，最低温度15摄氏度，空气质量优，紫外线指数强。预计25号，受内蒙中东部冷空气影响，气温将骤降至5摄氏度以下，同时可能会伴有短时强降雨，局部地区可达到40-70毫米。请听众朋友们在享受阳光沐浴的同时，提前做好防寒保暖工作，谨防不稳定气温给您的出行和身体带来不便。今天的天气预报节目就播报到这里，欢迎您收听本台的其他节目，我们明天再见！听众朋友们，大家好。今天是2015年4月23日，星期四。欢迎大家收听今天的《天气预报》。现在为您播报今天早上6点钟发布的鄂尔多斯天气预报。今天夜间到明天白天，晴转多云，西风一到二级，最高温度25摄氏度，最低温度15摄氏度，空气质量优，紫外线指数强。预计25号，受内蒙中东部冷空气影响，气温将骤降至5摄氏度以下，同时可能会伴有短时强降雨，局部地区可达到40 - 70毫米。请听众朋友们在享受阳光沐浴的同时，提前做好防寒保暖工作，谨防不稳定气温给您的出行和身体带来不便。今天的天气预报节目就播报到这里，欢迎您收听本台的其他节目，我们明天再见！？'
tts_format = 'mp3'
tts_sample = '16k'
if __name__ == "__main__":
    ensure_dir('../logs')
    rm_logs('../logs/')
    pid = 1
    wsP = Ws_parms(
        url=ws_url,
        appkey=appkey,
        secret=secret,
        pid=pid,
        vcn=vcn,
        text=text,
        tts_format=tts_format,
        tts_sample=tts_sample,
        user_id=user_id,
    )
    do_ws(wsP)
    print('test done')
    write_results(wsP)