from hashlib import md5
from typing import Callable, Optional, List
from flask import request


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
