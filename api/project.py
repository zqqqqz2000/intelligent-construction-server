import datetime
from typing import Dict, Optional, List

from flask import Blueprint

from dao.process import Process
from dao.project import Project
from dao.pu import PU
from dao.user import User
from global_var import db
from utils import json_api, with_token

project = Blueprint("project", __name__, url_prefix="/project")


@project.route('/get_project_from_uid', methods=['POST'])
@json_api
@with_token()
def get_project_from_uid(json: Dict, token_data: Dict):
    role: str = token_data['role']
    uid: int = token_data['uid']
    paginate = Project.query.filter(
        User.id == uid,
        User.role == role,
        PU.uid == User.id,
        PU.pid == Project.id,
    ).paginate(page=json['page'], per_page=20, error_out=False)
    result = paginate.items
    return {
        'success': True,
        'data': [
            p.jsonify() for p in result
        ],
        'total': paginate.pages,
        'current': paginate.page
    }


@project.route('/alter_project', methods=['POST'])
@json_api
@with_token('investor')
def alter_project(json: Dict, _: Dict):
    pid = json['id']
    project_item: Project = Project.query.filter_by(id=pid).first()
    project_item.pic = json['pic']
    project_item.lng = json['lng']
    project_item.lat = json['lat']
    project_item.cost = json['cost']
    project_item.scale = json['scale']
    project_item.describe = json['describe']
    project_item.complete_per = json['complete_per']
    project_item.name = json['name']
    try:
        db.session.commit()
    except Exception as error:
        return {'success': False, 'info': str(error)}
    return {'success': True}


@project.route('/get_project', methods=['POST'])
@json_api
def get_project(json: Dict):
    result: Optional[List[Project]]
    if 'pids' in json:
        paginate = Project.query.filter(
            Project.id.in_(json['pids'])
        ).pageinate(page=json['page'], per_page=20)
        result = paginate.items
    else:
        paginate = Project.query.pageinate(page=json['page'], per_page=20)
        result = paginate.items
    return {
        'success': True,
        'data': [
            p.jsonify() for p in result
        ],
        'total': paginate.pages,
        'current': paginate.page
    }


@project.route("/add_project", methods=['POST'])
@json_api
@with_token('investor')
def add_project(json: Dict, token_data: Dict):
    name: str = json['name']
    describe: str = json['describe']
    cost: int = json['cost']
    scale: int = json['scale']
    pic: int = json['pic']
    lng: int = json['lng']
    lat: int = json['lat']
    uid: int = token_data['uid']
    p: Project = Project(
        name=name,
        describe=describe,
        scale=scale,
        cost=cost,
        complete_per=0,
        pic=pic,
        lng=lng,
        lat=lat,
    )
    try:
        db.session.add(p)
        db.session.commit()
        pu: PU = PU(
            pid=p.id,
            uid=uid
        )
        db.session.add(pu)
        db.session.commit()
    except Exception as e:
        return {'success': False, 'info': '图片不存在或项目已存在'}
    return {'success': True, 'info': '项目添加成功'}


@project.route("/get_project_supervisors", methods=['POST'])
@json_api
@with_token('investor')
def get_project_supervisors(json: Dict, token_data: Dict):
    pid = json['id']
    invs: List[User] = User.query.filter(
        PU.pid == pid,
        PU.uid == User.id,
        User.role == 'supervisor',
    ).all()
    return {'success': True, 'supervisors': [inv.jsonify(['id', 'username', 'name', 'role']) for inv in invs]}


@project.route("/add_project_supervisor", methods=['POST'])
@json_api
@with_token('investor')
def add_project_supervisor(json: Dict, token_data: Dict):
    pid = json['id']
    username = json['username']
    user: User = User.query.filter_by(
        username=username,
        role='supervisor'
    ).first()
    if not user:
        return {'success': False, 'info': '该监理人不存在'}
    pu = PU(
        pid=pid,
        uid=user.id
    )
    try:
        db.session.add(pu)
        print(pu.uid, pu.pid)
        db.session.commit()
    except:
        return {'success': False, 'info': '无法将该监理人加入项目'}
    return {'success': True}


@project.route("/remove_project_supervisor", methods=['POST'])
@json_api
@with_token('investor')
def remove_project_supervisor(json: Dict, token_data: Dict):
    uid = json['id']
    pid = json['pid']
    try:
        pu = PU.query.filter_by(uid=uid, pid=pid).first()
        db.session.delete(pu)
        db.session.commit()
    except Exception as e:
        return {'success': False, 'info': '监理人不存在'}
    return {'success': True}


@project.route("/add_project_process", methods=['POST'])
@json_api
@with_token('supervisor')
def add_project_process(json: Dict, token_data: Dict):
    pid = json['pid']
    comment = json['comment']
    date = json['date']
    date_db_type = datetime.datetime.strptime(date.split('.')[0], "%Y-%m-%d %H:%M:%S").date()
    update_uid = token_data['uid']
    pic = json['pic']
    process = Process(pid=pid, comment=comment, date=date_db_type, update_uid=update_uid, pic=pic)
    try:
        db.session.add(process)
        db.session.commit()
    except:
        return {'success': False, 'info': '进度添加失败，请确保图片上传'}
    return {'success': True}


@project.route("/get_project_process", methods=['POST'])
@json_api
@with_token('supervisor')
def get_project_process(json: Dict, token_data: Dict):
    pid = json['pid']
    processes: List[Process] = Process.query.filter_by(
        pid=pid,
    ).all()
    return {'success': True, 'processes': [process.jsonify() for process in processes]}
