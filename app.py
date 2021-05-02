from flask import Flask
from flask_cors import CORS
import config
from api.communicate import communicate
from api.pic import pic
from api.login import login
from api.project import project
from dao.user import User
from global_var import db

app = Flask(__name__)
app.config.from_object(config)
CORS(app)
db.init_app(app)


def init_account():
    u = User(
        username='admin',
        password='21232f297a57a5a743894a0e4a801fc3',
        name='小明',
        role='investor'
    )
    u1 = User(
        username='admin1',
        password='21232f297a57a5a743894a0e4a801fc3',
        name='小方',
        role='supervisor'
    )
    db.session.add(u)
    db.session.add(u1)
    db.session.commit()


with app.app_context():
    from dao.pic import PIC as _
    from dao.project import Project as _
    from dao.process import Process as _
    from dao.pu import PU as _
    from dao.notice import Notice as _

    # db.drop_all()
    db.create_all()
    # init_account()


def blueprint_init():
    app.register_blueprint(login)
    app.register_blueprint(project)
    app.register_blueprint(pic)
    app.register_blueprint(communicate)


blueprint_init()
if __name__ == '__main__':
    app.run()
