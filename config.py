import random
import string

HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'intelligent_construction'
USERNAME = 'root'
PASSWORD = ''

DB_URI = "mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset=utf8".format(
    username=USERNAME,
    password=PASSWORD,
    host=HOST,
    port=PORT,
    db=DATABASE
)

SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True
SECRET_KEY = ''.join(random.sample(string.ascii_letters + string.digits, 32))
