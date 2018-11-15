from flask import Blueprint, request, jsonify
from bson import ObjectId
from settings import M_DB, RET

info = Blueprint('info', __name__)


@info.route('/user_info', methods=['POST'])
def user_info():
    user_id = request.form.get('user_id')

    res = M_DB.user.find_one({'_id': ObjectId(user_id)}, {'pwd': 0})

    if res:
        res['_id'] = str(res.get('_id'))

    RET['code'] = 0
    RET['msg'] = ''
    RET['data'] = res

    return jsonify(RET)
