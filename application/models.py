from application.database import db
from flask_security import UserMixin, RoleMixin

# create model for relationship between roles and users
roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


# create model for roles
class Role(db.Model, RoleMixin):
    """Model for roles. Each role can be assigned to multiple users."""
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.String(255))



# create  model for user that stores the type of user in roles
class User(db.Model, UserMixin):
    """Model for users. Each user can have multiple roles and book requests."""
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('user', lazy='dynamic'))
    

class BookRequest(db.Model):
    """Model for tracking requests for books. Each request is associated with a user and a book, and has a date when it was requested."""
    __tablename__ = 'book_request'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    date_requested = db.Column(db.Date)

    user = db.relationship('User', backref=db.backref('book_requests', lazy='dynamic'))
    book = db.relationship('Book', backref=db.backref('book_requests', lazy='dynamic'))

    def __repr__(self):
        return f'<Request {self.id}>'



# Association table for the many-to-many relationship between sections and books
sections_books = db.Table('sections_books',
                          db.Column('section_id', db.Integer(), db.ForeignKey('section.id')),
                          db.Column('book_id', db.Integer(), db.ForeignKey('book.id')))

class Section(db.Model):
    """Model for sections of the library. Each section can contain multiple books."""
    __tablename__ = 'section'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.Date, default=db.func.current_date())
    description = db.Column(db.Text)

    # Establishing many-to-many relationship with books
    books = db.relationship('Book', secondary=sections_books, backref=db.backref('sections', lazy='dynamic'))

    def __repr__(self):
        return f'<Section {self.name}>'

# Association table for the many-to-many relationship between books and authors
author_book = db.Table('author_book',
                        db.Column('author_id', db.Integer(), db.ForeignKey('author.id')),
                        db.Column('book_id', db.Integer(), db.ForeignKey('book.id')))

class Author(db.Model):
    """Model for authors of books. Each author can write multiple books."""
    __tablename__ = 'author'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)

    def __repr__(self):
        return f'<Author {self.name}>'

class Book(db.Model):
    """Model for books in the library. Each book can have multiple authors, be in multiple sections, and have multiple book requests."""
    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(255), nullable=False)
    content_url = db.Column(db.String, nullable=False)  # Assuming this is a URL to a PDF file
    description = db.Column(db.Text)
    date_published = db.Column(db.Date)
    num_pages = db.Column(db.Integer)
    avg_rating = db.Column(db.Float)

    # Establishing many-to-many relationship with authors
    authors = db.relationship('Author', secondary=author_book, backref=db.backref('books', lazy='dynamic'))

    def __repr__(self):
        return f'<Book {self.name}>'




