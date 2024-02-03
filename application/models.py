from application.database import db
from flask_security import UserMixin, RoleMixin
from sqlalchemy import CheckConstraint

# create model for relationship between roles and users
roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


# create model for roles
class Role(db.Model, RoleMixin):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.String(255))


# create  model for user that stores the type of user in roles
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))


# Association table for the many-to-many relationship between sections and books
sections_books = db.Table('sections_books',
                          db.Column('section_id', db.Integer(), db.ForeignKey('sections.id')),
                          db.Column('book_id', db.Integer(), db.ForeignKey('books.id')))

class Sections(db.Model):
    __tablename__ = 'sections'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.Date)
    description = db.Column(db.Text)

    # Establishing many-to-many relationship with books
    books = db.relationship('Books', secondary=sections_books, backref=db.backref('sections', lazy='dynamic'))

    def __repr__(self):
        return f'<Section {self.name}>'



# Association table for the many-to-many relationship between books and authors
authors_books = db.Table('authors_books',
                        db.Column('author_id', db.Integer(), db.ForeignKey('authors.id')),
                        db.Column('book_id', db.Integer(), db.ForeignKey('books.id')))

class Authors(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)

    def __repr__(self):
        return f'<Author {self.name}>'

class Books(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    content_url = db.Column(db.String)  # Assuming this is a URL to a PDF file
    description = db.Column(db.Text)
    avg_rating = db.Column(db.Float)

    # Establishing many-to-many relationship with authors
    authors = db.relationship('Authors', secondary=authors_books, backref=db.backref('books', lazy='dynamic'))


    def __repr__(self):
        return f'<Book {self.name}>'


# class Book_Requests(db.Model):
#     __tablename__ = 'book_requests'
#     id = db.Column(db.Integer, primary_key=True)
#     book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     date_created = db.Column(db.DateTime, nullable=False)


# class BookLog(db.Model):
#     __tablename__ = 'book_log'
#     id = db.Column(db.Integer, primary_key=True)
#     book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
#     issued_to = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     date_issued = db.Column(db.DateTime, nullable=False)
#     date_returned = db.Column(db.DateTime, nullable=False)