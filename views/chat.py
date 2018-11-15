from flask import Blueprint, request, jsonify
from settings import M_DB
from settings import RET
from bson import ObjectId

cht = Blueprint("cht", __name__)


@cht.route("/get_msg", methods=["POST"])
def get_msg():
    user_id = request.form.get("user_id")
    sender = request.form.get("sender")
    chat_window = M_DB.chat.find_one({"user_list": {"$all": [user_id, sender]}})
    new_msg = chat_window.get("chat_list")[-1]

    RET["code"] = 0
    RET["msg"] = ""
    RET["data"] = new_msg.get("msg")

    return jsonify(RET)
