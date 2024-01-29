from flask import Flask
from application.database import db
from application.models import *
from application.config import KEY, DB

from flask_security import UserMixin, RoleMixin

# create app instance
def create_app(KEY, DB):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
    with open(KEY) as f:
        key = f.readline()
        app.secret_key = bytes(key, 'utf-8')
    db.init_app(app)
    db.create_all()
    app.app_context().push()
    return app

app = create_app(KEY, DB)

from application.controllers import *

# app run   
if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        debug=True,
        port=8080
    )

