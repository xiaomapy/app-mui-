import os
import json
import requests

from uuid import uuid4

from settings import M_DB
from settings import XMLY_URL
from settings import AUDIO_FILE
from settings import AUDIO_IMG_FILE

content_url = "/ertong/4376210/16179170"
category = "erge"

pid = content_url.rsplit("/", 1)[-1]

song_url = XMLY_URL + pid + ".json"
content = requests.get(song_url)

content_dict = json.loads(content.content.decode("utf8"))  # Response.content方法

play_url = content_dict.get("play_path")
cover_url = content_dict.get("cover_url")

intro = content_dict.get("intro")
nickname = content_dict.get("nickname")
title = content_dict.get("title")

fill_name = "%s" % uuid4()
audio = "%s.mp3" % fill_name
image = "%s.jpg" % fill_name

audio_file = requests.get(play_url).content
with open(os.path.join(AUDIO_FILE, audio), 'wb') as f:
    f.write(audio_file)

image_file = requests.get(cover_url).content
with open(os.path.join(AUDIO_IMG_FILE, image), 'wb') as f:
    f.write(image_file)

content_info = {
    "title": title,
    "nickname": nickname,
    "avatar": image,
    "audio": audio,
    "intro": intro,
    "category": category,
    "play_count": 0
}

M_DB.sources.insert_one(content_info)
