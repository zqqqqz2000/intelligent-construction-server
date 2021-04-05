from global_var import db


class PIC(db.Model):
    __tablename__ = "pid"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    path = db.Column(db.VARCHAR(128), nullable=False)
