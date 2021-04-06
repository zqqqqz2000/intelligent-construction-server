from global_var import db
from utils import WithJsonifyModel


class Project(WithJsonifyModel, db.Model):
    __tablename__ = "project"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.VARCHAR(20), nullable=False, index=True, unique=True)
    describe = db.Column(db.VARCHAR(128), nullable=False)
    scale = db.Column(db.Integer, nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    complete_per = db.Column(db.Integer, nullable=False)
    pic = db.Column(db.Integer, db.ForeignKey("pic.id"), nullable=False)
