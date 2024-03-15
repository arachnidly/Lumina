from flask import request, jsonify
from flask_restful import Resource, reqparse, fields, marshal_with, abort
from application.database import db
from application.models import Section

# Fields schema for serialization
section_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'date_created': fields.DateTime(dt_format='iso8601'),
    'description': fields.String,
    'avg_rating': fields.Float
}

class SectionApi(Resource):
    # GET method to retrieve one or all sections
    @marshal_with(section_fields)
    def get(self, section_id=None):
        if section_id:
            section = Section.query.get_or_404(section_id)
            return section
        else:
            sections = Section.query.all()
            return sections

    # POST method to create a new section
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, required=True, help='Title is required')
        parser.add_argument('description', type=str, required=True, help='Description is required')
        args = parser.parse_args()

        # Check for duplicate title
        if Section.query.filter_by(title=args['title']).first():
            abort(400, message="A section with that title already exists.")

        section = Section(title=args['title'], description=args['description'])
        db.session.add(section)
        db.session.commit()

        return jsonify({'message': 'Section created successfully', 'section_id': section.id})

    # PUT method to update an existing section
    @marshal_with(section_fields)
    def put(self, section_id):
        section = Section.query.get_or_404(section_id)

        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str, required=True, help='Title is required')
        parser.add_argument('description', type=str, required=True, help='Description is required')
        args = parser.parse_args()

        if Section.query.filter(Section.id != section_id, Section.title == args['title']).first():
            abort(400, message="A section with that title already exists.")

        section.title = args['title']
        section.description = args['description']
        db.session.commit()

        return section

    # DELETE method to delete a section
    def delete(self, section_id):
        section = Section.query.get_or_404(section_id)
        # check if books in section are currently issued
        if section.books:
            for book in section.books:
                abort(400, message="Please log in as librarian and first delete all books in this section. Then this section can be deleted")
        else:
            db.session.delete(section)
            db.session.commit()

        return jsonify({'message': 'Section deleted successfully'})