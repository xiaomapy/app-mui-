from flask import Blueprint, request, jsonify
from settings import RET, M_DB
from views.register import get_md5

logning = Blueprint('login', __name__)


@logning.route('/login', methods=['POST'])
def login():
    '''
    登录验证
    :return:
    '''
    RET['code'] = 1
    RET['msg'] = '用户名密码输入错误'
    RET['data'] = {}

    username = request.form.get('username')
    pwd = request.form.get('pwd')
    pwd_md5 = get_md5(pwd)
    user_obj = M_DB.user.find_one({'name': username, 'pwd': pwd_md5})

    if user_obj:
        user_obj['_id'] = str(user_obj.get("_id"))
        RET['code'] = 0
        RET['msg'] = '欢迎登录'
        RET['data'] = {'user_id': user_obj.get("_id")}

    return jsonify(RET)
