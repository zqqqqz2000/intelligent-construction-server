from hashlib import md5
from typing import Callable, Optional, List, Dict
from flask import request
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from config import SECRET_KEY


def json_api(func: Callable):
    def inner_func(*args, **kwargs):
        return func(request.get_json(silent=True), *args, **kwargs)

    inner_func.__name__ = func.__name__
    return inner_func


def check_pwd(pwd: str, pwd_hash: str) -> bool:
    m = md5()
    m.update(pwd.encode())
    return m.hexdigest() == pwd_hash


class WithJsonifyModel:
    def jsonify(self, columns: Optional[List[str]] = None):
        raw_func_name_list = ['jsonify', 'metadata', 'query', 'query_class']
        all_columns = dir(self)
        all_columns = filter(lambda name: not name.startswith('_') and name not in raw_func_name_list, all_columns)
        if not columns:
            columns = all_columns
        return {k: self.__getattribute__(k) for k in columns}


def generate_auth_token(data: Dict, expiration=36000):
    s = Serializer(SECRET_KEY, expires_in=expiration)
    return s.dumps(data)


def with_token(role: Optional[str] = None):
    # 修饰器闭包
    def inner_back(func: Callable) -> Callable:
        # 函数闭包
        def inner_func(json: Dict, *args, **kwargs):
            # 修饰验证Token及角色
            s = Serializer(SECRET_KEY)
            try:
                data = s.loads(bytes.fromhex(json['token']))
                if role and data['role'] != role:
                    raise Exception('role exception')
            except Exception as ignore:
                return {'success': False, 'info': '登录凭证过期，请尝试重新登录'}
            return func(json, data, *args, **kwargs)
        inner_func.__name__ = func.__name__
        return inner_func
    return inner_back
