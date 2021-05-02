from typing import Dict

from flask import Blueprint

from dao.pu import PU
from dao.user import User
from global_var import db, r
from utils import json_api, with_token

communicate = Blueprint("communicate", __name__, url_prefix="/communicate")


@communicate.route('/get_chat_users', methods=['POST'])
@json_api
@with_token()
def get_chat_users(json: Dict, token_data: Dict):
    uid = token_data['uid']
    sub = db.session.query(PU.pid).filter(
        PU.uid == uid
    ).subquery()
    res = db.session.query(PU.uid).filter(
        PU.pid == sub.c.pid,
    ).all()
    return {'success': True, 'uid': [i[0] for i in res]}


@communicate.route('/get_communicate_account_info', methods=['POST'])
@json_api
@with_token()
def get_communicate_account_info(json: Dict, token_data: Dict):
    uid = json['uid']
    self_uid = token_data['uid']
    user: User = User.query.filter_by(id=uid).first()
    user_info: Dict = user.jsonify(['id', 'username', 'name', 'role'])
    user_info['message_num'] = r.llen(f"{uid}_to_{self_uid}")
    return {'success': True, 'info': user_info}


@communicate.route('/send_message_to', methods=['POST'])
@json_api
@with_token()
def send_message_to(json: Dict, token_data: Dict):
    other_uid = json['uid']
    data = json['data']
    self_uid = token_data['uid']
    r.rpush(f'{self_uid}_to_{other_uid}', data)
    return {'success': True}


@communicate.route('/get_message_from', methods=['POST'])
@json_api
@with_token()
def get_message_from(json: Dict, token_data: Dict):
    other_uid = json['uid']
    self_uid = token_data['uid']
    msg_len = r.llen(f"{other_uid}_to_{self_uid}")
    data = r.lrange(f"{other_uid}_to_{self_uid}", 0, msg_len)
    r.delete(f"{other_uid}_to_{self_uid}")
    return {'success': True, 'data': data}
