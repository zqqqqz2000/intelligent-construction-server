from flask import Blueprint

from dao.user import User
from utils import json_api, check_pwd

login = Blueprint("login", __name__, url_prefix="/login")


@login.route("/web_login", methods=['POST'])
@json_api
def web_login(json):
    username: str = json['username']
    password: str = json['password']
    u: User = User.query.filter_by(username=username).first()
    if u:
        if check_pwd(password, u.password):
            return {'success': True, 'info': '登录成功'}
    return {'success': False, 'info': '用户存在或密码错误'}
