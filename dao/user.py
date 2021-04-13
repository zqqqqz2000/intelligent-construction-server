from global_var import db
from utils import WithJsonifyModel


class User(WithJsonifyModel, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.VARCHAR(20), nullable=False, index=True, unique=True)
    password = db.Column(db.VARCHAR(128), nullable=False)
    name = db.Column(db.VARCHAR(10), nullable=False)
    role = db.Column(db.VARCHAR(10), nullable=False)
