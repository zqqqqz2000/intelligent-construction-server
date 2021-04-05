from flask import Flask

import config
from api.login import login
from global_var import db

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


def blueprint_init():
    app.register_blueprint(login)


if __name__ == '__main__':
    blueprint_init()
    app.run()
