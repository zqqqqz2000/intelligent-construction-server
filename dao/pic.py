from global_var import db
from utils import WithJsonifyModel


class PIC(WithJsonifyModel, db.Model):
    __tablename__ = "pic"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    path = db.Column(db.VARCHAR(128), nullable=False)
