import hashlib
from flask import Blueprint, request
from settings import M_DB

reg = Blueprint('reg', __name__)

usr_list = []


def get_md5(args):
    '''
    加密函数
    :param args:
    :return:
    '''
    m = hashlib.md5()
    m.update(args.encode("utf-8"))
    res = m.hexdigest()

    return res


@reg.route('/register', methods=['POST'])
def register():
    name = request.form.get('name')
    pwd = request.form.get('pwd')
    re_pwd_md5 = get_md5(pwd)
    nickname = request.form.get('nickname')
    age = request.form.get('age')
    tel = request.form.get('tel')
    usr_list.extend([name, pwd, nickname, age, tel])

    user_list = M_DB.user.find({'name':name})

    for user in user_list:
        if user.get('name') == name:
            return '用户名已存在'

    if all(usr_list):
        userInfo = {
            'name': name,
            'pwd': re_pwd_md5,
            'nickname': nickname,
            'age': age,
            'tel': tel

        }

        M_DB.user.insert_one(userInfo)
        return '注册成功'
    return '所填不能为空'
