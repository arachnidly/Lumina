from application.database import db
from flask_security import UserMixin, RoleMixin
from datetime import timedelta

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
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))
    books_requested = db.relationship('Book', secondary='book_request')
    books_borrowed = db.relationship('Book', secondary='book_log')



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
    """Model for the books in the library. Each book can be written by multiple authors and belong to multiple sections."""
    
    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content_url = db.Column(db.String, nullable=False)  # Assuming this is a URL to a PDF file
    description = db.Column(db.Text)
    bookcover_url = db.Column(db.String, nullable=False)
    avg_rating = db.Column(db.Float)

    # requested_by = db.relationship('User', secondary='book_request')

    is_borrowed = db.Column(db.Boolean, default=False)

    # Establishing many-to-many relationship with authors
    authors = db.relationship('Author', secondary=author_book, backref=db.backref('books', lazy='dynamic'))

    def __repr__(self):
        return f'<Book {self.name}>'


class BookRequest(db.Model):
    """Model for book requests. Each request is made by a user and can be for one book."""
    __tablename__ = 'book_request'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    date_requested = db.Column(db.Date, default=db.func.current_date())
    fulfilled = db.Column(db.Boolean, default=False)



class BookReview(db.Model):
    """Model for book ratings. Each rating is made by a user and can be for one book."""
    __tablename__ = 'book_review'

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    rater = db.Column(db.String, db.ForeignKey('user.username'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    date_rated = db.Column(db.Date, default=db.func.current_date())
    comment = db.Column(db.Text)

    
class BookLog(db.Model):
    """Model for book logs. Each log is made by a user and can be for one book."""
    __tablename__ = 'book_log'

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_borrowed = db.Column(db.Date, default=db.func.current_date())
    # set default return date to 7 days from date borrowed and update to actual return date if returned early
    return_date = db.Column(db.Date, default=db.func.current_date() + timedelta(days=7))
    # actual_return_date = db.Column(db.Date)
    returned = db.Column(db.Boolean, default=False)
