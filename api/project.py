from typing import Dict, Optional, List

from flask import Blueprint

from dao.project import Project
from global_var import db
from utils import json_api

project = Blueprint("project", __name__, url_prefix="/project")


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
            p.id for p in result
        ],
        'total': paginate.pages,
        'current': paginate.page
    }


@project.route("/add_project", methods=['POST'])
@json_api
def add_project(json: Dict):
    name: str = json['name']
    describe: str = json['describe']
    cost: int = json['cost']
    scale: int = json['scale']
    pic: int = json['pic']
    p: Project = Project(
        name=name,
        describe=describe,
        scale=scale,
        cost=cost,
        complete_per=0,
        pic=pic
    )
    try:
        db.session.add(p)
        db.session.commit()
    except Exception as e:
        return {'success': False, 'info': '图片不存在或项目已存在'}
    return {'success': True, 'info': '项目添加成功'}
