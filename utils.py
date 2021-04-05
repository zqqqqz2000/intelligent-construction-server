from hashlib import md5
from typing import Callable, Dict
from flask import request


def json_api(func: Callable):
    def inner_func(*args, **kwargs):
        return func(request.get_json(silent=True), *args, **kwargs)

    return inner_func


def check_pwd(pwd: str, pwd_hash: str) -> bool:
    m = md5()
    m.update(pwd.encode())
    return m.hexdigest() == pwd_hash
