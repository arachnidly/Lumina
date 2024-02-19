from application.database import db
# from flask_security import UserMixin, RoleMixin
from datetime import timedelta

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
    username = db.Column(db.String(30), nullable=False, unique=True)
    # email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))
    books_requested = db.relationship('Book', secondary='book_request')
    books_borrowed = db.relationship('Book', secondary='book_loan')


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

    def calculate_average_rating(self):
        # total_ratings is the numerical sum of all the avg rating of every book in the section.            
        total_ratings = sum(book.avg_rating for book in self.books if book.avg_rating is not None) 
        num_books = len([book for book in self.books if book.avg_rating is not None])
        if num_books > 0:
            self.avg_rating = total_ratings / num_books
        else:
            self.avg_rating = None

    # Establishing many-to-many relationship with books
    books = db.relationship('Book', secondary=sections_books)


# Association table for the many-to-many relationship between books and authors

# author_book = db.Table('author_book',
#                         db.Column('author_id', db.Integer(), db.ForeignKey('author.id'), primary_key=True),
#                         db.Column('book_id', db.Integer(), db.ForeignKey('book.id'), primary_key=True))

class Author(db.Model):
    """Model for authors of books. Each author can write multiple books."""
    __tablename__ = 'author'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)


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
    authors = db.relationship('Author', secondary='book_authors')
    avg_rating = db.Column(db.Float)

    # Method to calculate average rating
    def calculate_average_rating(self):
        total_ratings = sum(feedback.rating for feedback in self.book_feedback)
        num_ratings = len(self.book_feedback)
        if num_ratings > 0:
            self.avg_rating = total_ratings / num_ratings
        else:
            self.avg_rating = None

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
    date_requested = db.Column(db.Date, default=db.func.current_timestamp())
    fulfilled = db.Column(db.Boolean, default=False)


class BookFeedback(db.Model):
    """Model for book feedback provided by users."""
    __tablename__ = 'book_feedback'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Define relationship with User and Book
    # user = db.relationship('User', backref=db.backref('book_feedback', lazy='dynamic'))
    book = db.relationship('Book', backref=db.backref('book_feedback', lazy='dynamic'))


class BookLoan(db.Model):
    """Model for book loans. Each loan represents a book borrowed by a user."""
    __tablename__ = 'book_loan'

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    date_borrowed = db.Column(db.Date, default=db.func.current_date())
    return_date = db.Column(db.Date, default=db.func.current_date() + timedelta(days=7))
    returned = db.Column(db.Boolean, default=False)

    # Define the relationship with User and Book
    # user = db.relationship('User', backref=db.backref('book_loans', lazy='dynamic'))
    # book = db.relationship('Book', backref=db.backref('book_loans', lazy='dynamic'))



