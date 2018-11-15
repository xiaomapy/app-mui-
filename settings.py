import pymongo
import os

client = pymongo.MongoClient('127.0.0.1', port=27017)
M_DB = client.info

RET = {
    "code": 0,
    'msg': '欢迎登陆',
    'data': {}
}

# 歌曲url
XMLY_URL = "http://m.ximalaya.com/tracks/"

# 二维码URI
CREATE_QR_URL = "http://qr.liantu.com/api.php?text="

# 文件目录

AUDIO_FILE = os.path.join(os.path.dirname(__file__), 'audio')
CHAT_FILE = os.path.join(os.path.dirname(__file__),"chat")
AUDIO_IMG_FILE = os.path.join(os.path.dirname(__file__), 'audio_img')
DEVICE_CODE_PATH = os.path.join(os.path.dirname(__file__), "device_code")

# 百度ai
APP_ID = '11801619'
API_KEY = 'G37OerKlmaUWrFwizpCvfONf'
SECRET_KEY = 'w0URILF7WV9kiddK7dYxGPDFKKv4BvFs'
SPEECH = {
    "spd": 4,
    'vol': 7,
    "pit": 9,
    "per": 4
}