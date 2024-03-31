from flask import Flask
from application.database import db
from flask_restful import Api
from flask_cors import CORS
from application.models import *
from application.config import UPLOAD_FOLDER, KEY, DB


# create app instance
def create_app(UPLOAD_FOLDER, KEY, DB):
    app = Flask(__name__)
    CORS(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
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
from application.api import SectionApi


# create api instance and add resources

api = Api(app)
app.app_context().push()

api.add_resource(SectionApi, '/api/sections', '/api/sections/<int:section_id>')


# app run   
if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        debug=True,
        port=8080
    )

