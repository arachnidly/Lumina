from flask import Flask
from application.database import db
from flask_restful import Api
from application.models import *
from application.config import UPLOAD_FOLDER, KEY, DB
# from flask_security import UserMixin, RoleMixin, login_required, Security, SQLAlchemyUserDatastore, roles_required


# create app instance
def create_app(UPLOAD_FOLDER, KEY, DB):
    app = Flask(__name__)
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite3'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dummy.sqlite3'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    with open(KEY) as f:
        key = f.readline()
        app.secret_key = bytes(key, 'utf-8')
    db.init_app(app) # Initialize the database
    api = Api(app)
    app.app_context().push()
    return app, api

app, api = create_app(UPLOAD_FOLDER, KEY, DB)

from application.controllers import *


# import apis
# from application.api import UserAPI, ExampleAPI, ...


# create api instance and add resources

# api = Api(app)
# app.app_context().push()

# api.add_resource(SectionApi, '/section', '/user/<int:user_id>')

#

# app run   
if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        debug=True,
        port=8080
    )

