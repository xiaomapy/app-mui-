from flask import Blueprint, request, jsonify
from settings import M_DB
from settings import RET
from bson import ObjectId

fri = Blueprint("fri", __name__)


@fri.route("/friend_list", methods=["POST"])
def friend_list():
    user_id = request.form.get("user_id")
    res = M_DB.user.find_one({"_id": ObjectId(user_id)})
    friend_list = res.get("friend_list")

    RET["code"] = 0
    RET["msg"] = ""
    RET["data"] = friend_list

    return jsonify(RET)