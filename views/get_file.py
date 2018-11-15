import os

from flask import Blueprint, send_file

from settings import AUDIO_FILE
from settings import AUDIO_IMG_FILE
from settings import CHAT_FILE

getfile = Blueprint('getfile', __name__)


@getfile.route('/get_audio/<filename>')
def get_audio(filename):
    audio = os.path.join(AUDIO_FILE, filename)
    return send_file(audio)


@getfile.route('/get_image/<filename>')
def get_image(filename):
    image = os.path.join(AUDIO_IMG_FILE, filename)
    return send_file(image)


@getfile.route('/get_chat/<filename>')
def get_chat(filename):
    chat = os.path.join(CHAT_FILE, filename)
    return send_file(chat)