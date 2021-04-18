from global_var import db
from utils import WithJsonifyModel


class Process(WithJsonifyModel, db.Model):
    __tablename__ = "process"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pid = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=False)
    comment = db.Column(db.VARCHAR(128), nullable=False)
    date = db.Column(db.Date, nullable=False)
    update_uid = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    pic = db.Column(db.Integer, db.ForeignKey("pic.id"), nullable=False)
