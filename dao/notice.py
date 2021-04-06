from global_var import db
from utils import WithJsonifyModel


class Notice(WithJsonifyModel, db.Model):
    __tablename__ = "notice"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    msg = db.Column(db.VARCHAR(128), nullable=False)
    pid = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=False)
    notice_uid = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
