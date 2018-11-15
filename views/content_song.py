from flask import Blueprint, jsonify, request
from bson import ObjectId

from settings import M_DB
from settings import RET

song_cont = Blueprint('song_cont', __name__)


@song_cont.route('/song_list', methods=['POST'])
def song_list():
    '''
    前端main页面获取歌曲列表，视图函数
    :return:
    '''
    song_list = list(M_DB.sources.find({}))  # 将Cursor object对象，转化成list

    for index, song in enumerate(song_list):
        song_list[index]['_id'] = str(song.get('_id'))  # 将每一个ObjectId转化成str

    RET['code'] = 0
    RET['msg'] = ''
    RET['data'] = song_list

    return jsonify(RET)


@song_cont.route("/song_one", methods=["POST"])
def song_one():
    '''
    点击播放具体一首歌，视图函数
    :return:
    '''
    song_id = request.form.get('content_id')
    res = M_DB.sources.find_one({"_id": ObjectId(song_id)})

    res["_id"] = str(res["_id"])

    RET["code"] = 0
    RET["msg"] = ""
    RET["data"] = res

    return jsonify(RET)


def _song_one(music_id):
    '''
    玩具发来请求、播放歌曲时，调用查询时那首歌；不是视图函数。
    :param music_id:
    :return:
    '''
    res = M_DB.sources.find_one({"_id": ObjectId(music_id)})
    return res
