from application.database import db
# from flask_security import UserMixin, RoleMixin
from datetime import timedelta
from sqlalchemy import text

# create model for relationship between roles and users
roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

# create model for roles
# class Role(db.Model, RoleMixin):
class Role(db.Model):
    """Model for roles. Each role can be assigned to multiple users."""
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.String(255))

# create  model for user that stores the type of user in roles
# class User(db.Model, UserMixin):
class User(db.Model):
    """Model for users. Each user can have multiple roles and book requests."""
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    quota = db.Column(db.Integer, default=0, nullable=False)
    username = db.Column(db.String(30), nullable=False, unique=True)
    # email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))
    books_requested = db.relationship('Book', secondary='book_request')
    
# Association table for the many-to-many relationship between sections and books
sections_books = db.Table('sections_books',
                          db.Column('section_id', db.Integer(), db.ForeignKey('section.id')),
                          db.Column('book_id', db.Integer(), db.ForeignKey('book.id')))

class Section(db.Model):
    """Model for sections of the library. Each section can contain multiple books."""
    __tablename__ = 'section'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.Date, default=db.func.current_date())
    description = db.Column(db.Text)
    avg_rating = db.Column(db.Float)
    # Establishing many-to-many relationship with books
    books = db.relationship('Book', secondary=sections_books)
    


class Author(db.Model):
    """Model for authors of books. Each author can write multiple books."""
    __tablename__ = 'author'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    books = db.relationship('Book', secondary='book_authors', viewonly=True)


class Book(db.Model):
    """Model for the books in the library. Each book can be written by multiple authors and belong to multiple sections."""
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content_link = db.Column(db.String, nullable=False)  # Assuming this is a URL to a PDF file
    description = db.Column(db.Text)
    bookcover_link = db.Column(db.String, nullable=False)
    section_id = db.Column(db.Integer, db.ForeignKey('section.id'))
    # author = db.Column(db.String, db.ForeignKey("author.name"), nullable=False)
    author = db.relationship('Author', secondary='book_authors')
    available = db.Column(db.Boolean, default=True)
    avg_rating = db.Column(db.Float)


# Association table for the many-to-many relationship between books and authors
class BookAuthors(db.Model):
    __tablename__ = 'book_authors'
    author_id = db.Column(db.Integer, db.ForeignKey("author.id"), primary_key=True, nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), primary_key=True, nullable=False)

class BookRequest(db.Model):
    """Model for book requests. Each request is made by a user and can be for one book."""
    __tablename__ = 'book_request'

    id = db.Column(db.Integer, primary_key=True)

    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    book_title = db.Column(db.String(255)) # for ease of display
    book_author = db.Column(db.String(255)) # for ease of display
    username = db.Column(db.String(30)) # for ease of display
    date_requested = db.Column(db.Date, default=db.func.current_date())
    issued = db.Column(db.Boolean, default=False)
    date_issued = db.Column(db.Date)
    date_due = db.Column(db.Date)
    auto_return_timestamp = db.Column(db.DateTime)


class ReadingHistory(db.Model):
    """Model for reading history. Each history is made by a user and can be for one book."""
    __tablename__ = 'reading_history'

    id = db.Column(db.Integer, primary_key=True)

    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    book_title = db.Column(db.String(255)) # for ease of display
    book_author = db.Column(db.String(255)) # for ease of display
    username = db.Column(db.String(30)) # for ease of display
    date_issued = db.Column(db.Date)
    date_returned = db.Column(db.Date, default=db.func.current_date())


class BookRating(db.Model):
    """Model for storing rating between 1-5 for a book provided reader."""
    __tablename__ = 'book_rating'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    rating = db.Column(db.Integer, nullable=False)
    book = db.relationship('Book', backref='ratings')


class BooksBought(db.Model):
    """Model for storing books bought by a user."""
    __tablename__ = 'books_bought'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))