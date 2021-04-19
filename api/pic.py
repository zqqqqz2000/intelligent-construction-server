from flask import Blueprint, request
import os

from dao.pic import PIC
from global_var import db
from utils import json_api

pic = Blueprint('pic', __name__, url_prefix='/pic')


@pic.route("/upload", methods=['POST'])
def upload():
    pic_file = request.files.get('pic')
    file_sub = pic_file.filename.split('.')[-1]
    file_name = os.urandom(32).hex() + f'.{file_sub}'
    pic_file.save(f'static/pics/{file_name}')
    pic_item = PIC(
        path=file_name
    )
    db.session.add(pic_item)
    db.session.commit()
    return {'success': True, 'id': pic_item.id}


@pic.route("/get_img", methods=['POST'])
@json_api
def get_img(json):
    id_ = json['id']
    pic_item: PIC = PIC.query.filter_by(id=id_).first()
    if pic_item:
        return {'success': True, 'pic_path': pic_item.path}
    return {'success': False, 'info': '图片不存在'}
