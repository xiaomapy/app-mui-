from flask import Blueprint, request, jsonify
from settings import M_DB
from settings import RET
from bson import ObjectId

devs = Blueprint('devs', __name__)


@devs.route("/check_code", methods=["POST"])
def check_code():
    '''
    开机二维码检测
    :return:
    '''
    device_id = request.form.get("device_id")

    if M_DB.devices.find_one({"device_id": device_id}):  # 查找玩具芯片编号
        toy_info = M_DB.toys.find_one({"device_id": device_id})  # 查看玩具是否绑定用户

        if not toy_info:
            RET["code"] = 0
            RET["msg"] = "感谢购买本公司产品"
            RET["data"] = {}
        if toy_info:
            pass
    else:
        RET["code"] = 2
        RET["msg"] = "你买假货了，我们只识别我们自己的设备，快去买正版！"
        RET["data"] = {}
    return jsonify(RET)


@devs.route("/bind_toy", methods=["POST"])
def bind_toy():
    '''
    绑定玩具
    :return:
    '''
    chat_window = M_DB.chat.insert_one({})
    chat_id = chat_window.inserted_id  # 聊天id

    user_id = request.form.get("user_id")

    res = M_DB.user.find_one({"_id": ObjectId(user_id)})
    print(user_id)
    device_id = request.form.get("device_id")
    toy_name = request.form.get("toy_name")
    baby_name = request.form.get("baby_name")
    remark = request.form.get("remark")
    gender = request.form.get("gender")
    print(gender,type(gender))
    toy_info = {
        "device_id": device_id,
        "toy_name": toy_name,
        "baby_name": baby_name,
        "gender": gender,
        "avatar": "boy.jpg" if gender == 1 else "girl.jpg",
        "bind_user": str(res.get("_id")),  # 绑定用户

        "friend_list": [{  # 玩具添加好友
            "friend_id": str(res.get("_id")),
            "friend_name": res.get("nickname"),
            "friend_remark": remark,  # 玩具主人对您的称呼
            "friend_avatar": res.get("avatar"),
            "friend_chat": str(chat_id),
        }]

    }

    toy_res = M_DB.toys.insert_one(toy_info)

    if res.get("friend_list"):  # 用户添加好友
        res["bind_toy"].append(str(toy_res.inserted_id))
        res["friend_list"].append({
            "friend_id": str(toy_res.inserted_id),
            "friend_name": toy_name,
            "friend_remark": baby_name,
            "friend_avatar": toy_info.get("avatar"),
            "friend_chat": str(chat_id),
        })
    else:
        res["bind_toy"] = [str(toy_res.inserted_id)]
        res["friend_list"] = [{
            "friend_id": str(toy_res.inserted_id),
            "friend_name": toy_name,
            "friend_remark": baby_name,
            "friend_avatar": toy_info.get("avatar"),
            "friend_chat": str(chat_id),
        }]

    M_DB.user.update_one({"_id": ObjectId(user_id)}, {"$set": res})
    M_DB.chat.update_one({"_id": chat_id}, {
        "$set":
            {"user_list":
                 [str(toy_res.inserted_id),
                  str(res.get("_id"))]}
    })

    RET["code"] = 0
    RET["msg"] = "绑定成功"
    RET["data"] = {}

    return jsonify(RET)
