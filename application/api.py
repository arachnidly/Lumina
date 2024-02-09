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


class UserAPI(Resource):

    @marshal_with(user_fields)
    def get(self, username):
        user = User.query.filter_by(username=username).first()
        if user:
            return user
        else:
            raise NotFoundError(404, "User not found")
    
    @marshal_with(user_fields)
    def post(self):
        user = User.query.filter_by(username=['username']).first()
        if user:
            raise DuplicationError(400, "User already exists")
        else:
            user = User(username=request.json['username'])
            db.session.add(user)
            db.session.commit()
            return user, 201
        
    # @marshal_with(user_fields)
    # def put(self, username):
    #     user = User.query.filter_by(username=username).first()
    #     if user:
    #         user.username = request.json['username']
    #         db.session.commit()
    #         return user
    #     else:
    #         raise NotFoundError(404, "User not found")
        