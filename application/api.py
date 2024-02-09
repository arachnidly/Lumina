from flask_restful import Resource, fields, marshal_with, request, reqparse
from application.database import db
from application.models import *
from application.controllers import *
from application.validation import *
from application.config import UPLOAD_FOLDER

user_fields = {
    'id': fields.Integer,
    'username': fields.String
}

# create api instance and add resources for user
class UserAPI(Resource):
    @marshal_with(user_fields)
    def get(self, username):
        user = User.query.filter_by(username=username).first()
        if user is None:
            raise NotFoundError(404, "User not found")
        return user
    def put(self, username):
        user = User.query.filter_by(username=username).first()
        if user is not None:
            raise DuplicationError(40, "User not found")
        user.username = request.json['username']
        db.session.commit()
        return user, 201
    def delete(self, username):
        user = User.query.filter_by(username=username).first()
        if user is None:
            raise NotFoundError(404, "User not found")
        db.session.delete(user)
        db.session.commit()
        return '', 204
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, help='Username is required')
        parser.add_argument('password', type=str, required=True, help='Password is required')
        args = parser.parse_args()
        username = args['username']
        password = args['password']
        user = User.query.filter_by(username=username).first()
        if user is not None:
            raise DuplicationError(409, "User already exists")
        user = User(username=username, password=password)
        user.roles.append(Role.query.filter_by(name='user').first())
        db.session.add(user)
        db.session.commit()
        return user, 201


sections_fields = {
    'id': fields.Integer,
    'name': fields.String
}

class SectionAPI(Resource):
    def get(self, section_id):
        section = Section.query.filter_by(id=section_id).first()
        if section is None:
            raise NotFoundError(404, "Section not found")
        return section
    def put(self, section_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='Name is required')
        args = parser.parse_args()
        name = args['name']
    
        section = Section.query.filter_by(id=section_id).first()
        if section is None:
            raise NotFoundError(404, "Section not found")
        
        section.name = name
        db.session.commit()
        return section, 200


    def delete(self, section_id):
        section = Section.query.filter_by(id=section_id).first()
        if section is None:
            raise NotFoundError(404, "Section not found")
        db.session.delete(section)
        db.session.commit()
        return '', 204
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='Name is required')
        args = parser.parse_args()
        name = args['name']
        section = Section.query.filter_by(name=name).first()
        if section is not None:
            raise DuplicationError(409, "Section already exists")
        section = Section(name=name)
        db.session.add(section)
        db.session.commit()
        return section, 201