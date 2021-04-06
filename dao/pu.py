from global_var import db
from utils import WithJsonifyModel


class PU(WithJsonifyModel, db.Model):
    __tablename__ = "pu"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pid = db.Column(db.Integer, db.ForeignKey("project.id"), nullable=False)
    uid = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
