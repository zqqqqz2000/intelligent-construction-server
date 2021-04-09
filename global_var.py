from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
auth = HTTPBasicAuth()
