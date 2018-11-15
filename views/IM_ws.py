import json
import os

from flask import Flask, request
from geventwebsocket.websocket import WebSocket
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer

from uuid import uuid4
from bson import ObjectId

from settings import CHAT_FILE
from settings import M_DB
from utils import baidu_ai

app = Flask(__name__)

user_socket_dict = {}


@app.route("/toy/<tid>")
def toy(tid):
    '''
    玩具和后台的链接
    :param tid:
    :return:
    '''
    user_socket = request.environ.get("wsgi.websocket")  # type:WebSocket
    if user_socket:
        user_socket_dict[tid] = user_socket
        print(user_socket_dict)

    while True:
        msg = user_socket.receive()
        print(msg)
        if type(msg) == bytearray:
            with open("123.wav" "wb") as f:
                f.write(msg)


@app.route("/app/<uid>")
def user_app(uid):
    '''
    手机app和后台建立链接;手机端的app发起一个请求；我们send一条数据给玩具（web页面），让玩具来唱歌；
    :param uid:
    :return:
    '''
    user_socket = request.environ.get("wsgi.websocket")  # type:WebSocket
    if user_socket:
        user_socket_dict[uid] = user_socket
        print(user_socket_dict)
    file_name = ""
    to_user = ""
    while True:
        msg = user_socket.receive()  # {muisc_id:xxx,toy_id:yyy,msg_type:music/chat}
        if type(msg) == bytearray:
            file_name = "%s.amr" % uuid4()
            file_path = os.path.join(CHAT_FILE, file_name)
            with open(file_path, "wb") as f:
                f.write(msg)

            os.system("ffmpeg -i %s %s.mp3" % (file_path, file_path))
        else:
            msg_dict = json.loads(msg)

            to_user = msg_dict.get("to_user")
            if msg_dict.get("msg_type") == "music":
                other_user_socket = user_socket_dict.get(to_user)  # 玩具端的一个socket
                send_str = {
                    "code":0,
                    "from_user":uid,
                    "msg_type":"music",
                    "data":msg_dict.get("data")
                }
                other_user_socket.send(json.dumps(send_str))
                to_user = ""

        if file_name and to_user:

            res = M_DB.toys.find_one({"_id": ObjectId(to_user)})
            fri = [i.get("friend_remark") for i in res.get("friend_list") if i.get("friend_id") == uid][0]
            msg_file_name = baidu_ai.Text_to_speech("你有来自%s的消息" % fri)

            other_user_socket = user_socket_dict.get(to_user)

            send_str = {
                "code": 0,
                "from_user": uid,
                "msg_type": "chat",
                "data": msg_file_name
            }

            other_user_socket.send(json.dumps(send_str))  # 发给玩具，{哪个app发来的}  toy的websocket发送数据
            file_name = ""
            to_user = ""


if __name__ == '__main__':
    http_server = WSGIServer(("0.0.0.0", 8090), app, handler_class=WebSocketHandler)
    http_server.serve_forever()
