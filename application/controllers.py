from flask import request, render_template, redirect, url_for, session
# from flask_security import Security, UserMixin, RoleMixin, login_required, roles_required
from flask import current_app as app
from application.models import *
from application.config import *
import os

import datetime

# home page
@app.route('/', methods=['GET', 'POST'])
def home():
    # if user isn't logged in, redirect to welcome page with login button
    if "user" in session:
    # role = session['user_role']
        user = User.query.filter_by(username=session['user']).first()
        print(user.books_requested)
        roles = []
        for role in user.roles:
            roles.append(role.name)
        
        all_book_requests = BookRequest.query.filter_by(issued=False).all()
        user_book_requests = BookRequest.query.filter_by(user_id=user.id, issued=False).all()
        all_book_loans = BookRequest.query.filter_by(issued=True, returned=False).all()
        user_book_loans = BookRequest.query.filter_by(user_id=user.id, issued=True, returned=False).all()
        if roles[0] == 'admin':
            return render_template('librariandashboard.html', title='Librarian Dashboard', roles=roles, user=session['user'], book_requests=all_book_requests, book_loans=all_book_loans)
        else:
            return render_template('userdashboard.html', title='Dashboard', roles=roles, user=session['user'], book_requests=user_book_requests, book_loans=user_book_loans)
        
    else:
        return render_template('welcome.html', title='Welcome')

# login page
@app.route("/login", methods=['GET', 'POST'])
def login():
    if 'user' in session:
        return redirect("/")
    else:
        if request.method == 'GET':
            return render_template('login.html', title="Login")  # Render the template with the 'lib' value
        if request.method == 'POST':
            username = request.form["username"].lower()
            password = request.form["password"]
            valid_user = User.query.filter_by(username=username).first()
            if valid_user is None:
                return render_template("login.html", username_error=True, title="Login")
            if valid_user.password != password:
                return render_template('login.html', pwd_error=True, title="Login")
            session['user'] = username
            session['user_role'] = valid_user.roles[0].name
            return redirect("/")

@app.route("/librarianlogin", methods=['GET', 'POST'])
def librarianlogin():
    if 'user' in session:
        return redirect("/")
    else:
        if request.method == 'GET':
            return render_template('librarianlogin.html', title="Librarian Login")  # Render the template with the 'lib' value
        if request.method == 'POST':
            username = request.form["username"].lower()
            password = request.form["password"]
            valid_user = User.query.filter_by(username=username).first()
            if valid_user is None:
                return render_template("librarianlogin.html", username_error=True, title="Librarian Login")
            if valid_user.password != password:
                return render_template('librarianlogin.html', pwd_error=True, title="Librarian Login")
            if valid_user.roles[0].name != 'admin':
                return render_template('librarianlogin.html', auth_error=True, title="Librarian Login")
            session['user'] = username
            session['user_role'] = valid_user.roles[0].name
            return redirect("/")

# user sign-up page
@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if 'user' in session:
        return redirect("/")
    else:
        if request.method == "GET":
            return render_template('signup.html', title='Sign Up')
        if request.method == 'POST':
            # get form data
            username = request.form['username'].lower()
            password = request.form['password']
            password2 = request.form['password2']
            # check if passwords match
            if password != password2:
                return render_template('signup.html', pwd_error = True)
            user = User.query.filter_by(username=username).first()
            if user is not None:
                return render_template('signup.html', username_error=True)
            # create user
            user = User(username=username, password=password)
            user.roles.append(Role.query.filter_by(name='user').first())
            db.session.add(user)
            db.session.commit()
            session['user'] = username
            session['user_role'] = user.roles[0].name
            return redirect("/")

# user dashboard
@app.route("/user=<username>", methods=['GET', 'POST'])
def user_home(username):
    if "user" in session and username == session['user']:
        user = User.query.filter_by(username=username).first()

        
        if request.method == 'GET':
            return render_template('userdashboard.html', title='Dashboard', user=session['user'], role=session['user_role'])
        if request.method == 'POST':
            return redirect("/")
    else:
        return redirect("/")

# logout
@app.route('/logout', methods = ["GET"])
def logout():
    if "user" in session:
        session.pop("user", None)
    return redirect(url_for("home")) 


# search page
@app.route("/search", methods=['GET', 'POST'])
def search():
    if "user" in session:
        user = User.query.filter_by(username=session['user']).first()
        roles = []
        for role in user.roles:
            roles.append(role.name)
        if request.method == 'GET':
            return render_template('search.html', title='Search', user=session['user'], role=roles[0], roles=roles)
        if request.method == 'POST':
            search_term = request.form['search']
            # books = Book.query.filter(Book.title.ilike(f'%{search_term}%')).all()
            # return render_template('search.html', title='Search', books=books)
            return render_template('search.html', title='Search', user=session['user'], role=roles[0], roles=roles, search_term=search_term)
    else:
        return redirect("/")
    
# manage
@app.route("/manage")
def manage():
    if "user" in session:
        user = User.query.filter_by(username=session['user']).first()
        roles = []
        for role in user.roles:
            roles.append(role.name)
        
        if roles[0] == 'admin':
            sections = db.session.query(Section).order_by(Section.id.desc()).all()
            

            return render_template('manage.html', title='Manage Catalog', user=session['user'], role=session['user_role'], sections=sections)
    else:
        return redirect("/")

# browse
@app.route("/browse")
def browse():
    if "user" in session:
        sections = db.session.query(Section).order_by(Section.id.desc()).all()

        return render_template('browse.html', title='Browse', user=session['user'], role=session['user_role'], sections=sections)
    else:
        return redirect("/")

# add section
@app.route("/addsection", methods=['GET','POST'])
def add_section():
    if "user" in session and session['user_role'] == 'admin':
        user = User.query.filter_by(username=session['user']).first()
        roles = []
        for role in user.roles:
            roles.append(role.name)
        if request.method == 'GET':
            # sections = Section.query.all()
            return render_template('addsection.html', title='Add Section', user=session['user'], role=session['user_role'], roles=roles)
        if request.method == 'POST':
            title = request.form['sectionTitle'].title()
            description = request.form['sectionDescription']
            if title:  # Basic validation to check if the section title is provided in the form
                section = Section.query.filter_by(title=title).first()
                if section:
                    return render_template('addsection.html', section_title_error=True, title='Add Section', user=session['user'], role=session['user_role'], section=section, roles=roles)
                section = Section(title=title, description=description)
                db.session.add(section)
                db.session.commit()
                # Redirect back to the manage catalog page with a success message
                # sections = Section.query.all()
                return redirect(url_for('manage'))
    else:
        return redirect("/")
    


# section page
@app.route("/section/<section_id>", methods=['GET', 'POST'])
def section(section_id):
    if "user" in session:
        user = User.query.filter_by(username=session['user']).first()
        roles = []
        for role in user.roles:
            roles.append(role.name)
        section = Section.query.filter_by(id=section_id).first()
        books = Book.query.filter_by(section_id=section_id).order_by(Book.id.asc()).all()
        section_book_count = len(books)

        if request.method == 'GET':
            book_requests = BookRequest.query.filter_by(issued=0).all()
            return render_template('section.html', title=section.title, user=session['user'], roles=roles, role=roles[0], section=section, books=books, book_count=section_book_count)
        if request.method == 'POST':
            book_requests = BookRequest.query.filter_by(issued=False).all()

            return redirect("/")
    else:
        return redirect("/")

# edit section
@app.route("/section=<section_id>/edit", methods=['GET','POST'])
def edit_section(section_id):
    section = Section.query.filter_by(id=section_id).first()

    if "user" in session and session['user_role'] == 'admin':
        if request.method == 'GET':
            return render_template('editsection.html', title='Edit Section', user=session['user'], role=session['user_role'], section=section)
        elif request.method == 'POST':
            section.title = request.form['sectionTitle'].title()
            section.description = request.form['sectionDescription']
            db.session.commit()
            return redirect(url_for('section', section_id=section_id))
    else:
        return redirect("/")

# delete section
@app.route("/section=<section_id>/delete", methods=['GET','POST'])
def delete_section(section_id):
    section = Section.query.filter_by(id=section_id).first()
    if "user" in session and session['user_role'] == 'admin':
        if request.method == 'GET':
            return render_template('deletesection.html', title='Delete Section', user=session['user'], role=session['user_role'], section=section)
        elif request.method == 'POST':
            sections_books = Book.query.filter_by(section_id=section_id).all()
            for book in sections_books:
                book = BookRequest.query.filter_by(book_id=book.id).first()
                if book:
                    return redirect(url_for('section', section_id=section_id, error='Section cannot be deleted because it contains books that have been requested.'))
                db.session.delete(book)
                # db.session.commit()

            db.session.delete(section)
            db.session.commit()
            return redirect(url_for('manage'))
    else:
        return redirect("/")

# add book
@app.route("/section=<section_id>/addbook", methods=['GET','POST'])
def add_book(section_id):
    if "user" in session and session['user_role'] == 'admin':
        section = Section.query.filter_by(id=section_id).first()
        
        if request.method == 'GET':
            return render_template('addbook.html', title='Add Book', user=session['user'], role=session['user_role'], section=section)
        if request.method == 'POST':
            book_title = request.form['bookTitle'].upper()
            bt = book_title.lower()
            book_content = str(bt).replace(" ", "_")
            book_description = request.form['bookDescription']
            book_cover = str(bt).replace(" ", "_")
            book_pdf = request.files['bookFile']
            book_cover_img = request.files['bookCover']
            authors = request.form['bookAuthor'].title().split(',')
            for author in authors:
                authorname = Author.query.filter_by(name=author).first()
                if authorname is None:
                    auth = Author(name=author)
                    db.session.add(auth)
                    db.session.commit()
            book = Book.query.filter_by(title=book_title, section_id=section_id).first()
            if book:
                return render_template('addbook.html', book_title_error=True, title='Add Book', user=session['user'], role=session['user_role'], section=section, book=book)
            else:
                book = Book(title=book_title, section_id=section_id, description=book_description, content_link=book_content, bookcover_link=book_cover)
                section.books.append(book)
                for author in authors:
                    author = Author.query.filter_by(name=author).first()
                    book.authors.append(author)

                # section.books.append()

                book_pdf.save(os.path.join(app.config['UPLOAD_FOLDER'] + "pdf/" + book_content + ".pdf"))
                book_cover_img.save(os.path.join(app.config['UPLOAD_FOLDER'] + "img/" + book_cover + ".jpg"))
                db.session.add(book)
                db.session.commit()
                return redirect(url_for('section', section_id=section_id, success='Book added successfully!'))
            
# book
@app.route("/book/<book_id>", methods=['GET', 'POST'])
def book(book_id):
    book = Book.query.filter_by(id=book_id).first()

    if "user" in session:
        user = User.query.filter_by(username=session['user']).first()

        quota = user.quota
        roles = []
        for role in user.roles:
            roles.append(role.name)
        section = Section.query.filter_by(id=book.section_id).first()

        requested = False
        book_request = BookRequest.query.filter_by(book_id=book_id).first()
        if book_request:
            requested = True
        if request.method == 'GET':
            return render_template('book.html', title=book.title, user=session['user'], quota=quota, roles=roles, book=book, img=book.bookcover_link, section=section, requested=requested, book_request=book_request)
        if request.method == 'POST':
            
            return redirect("/")
    else:
        return redirect("/")
    
# edit book
@app.route("/book=<book_id>/edit", methods=['GET','POST'])
def edit_book(book_id):
    book = Book.query.filter_by(id=book_id).first()

    if "user" in session and session['user_role'] == 'admin':
        if request.method == 'GET':
            return render_template('editbook.html', title='Edit Book', user=session['user'], role=session['user_role'], book=book)
        elif request.method == 'POST':
            authors = request.form['bookAuthor'].title().split(',')
            for author in authors:
                authorname = Author.query.filter_by(name=author).first()
                if not authorname:
                    authorname = Author(name=author)
                    db.session.add(authorname)
                    db.session.commit()
            book.title = request.form['bookTitle'].upper()
            book.description = request.form['bookDescription']
            book.authors.clear()
            for author in authors:
                book.authors.append(Author.query.filter_by(name=author).first())
            db.session.commit()
            return redirect(url_for('book', book_id=book_id, success='Book updated successfully!'))
    else:
        return redirect("/")
    
# delete book
@app.route("/book=<book_id>/delete", methods=['GET','POST'])
def delete_book(book_id):
    book = Book.query.filter_by(id=book_id).first()
    section_id = book.section_id
    if "user" in session and session['user_role'] == 'admin':
        if request.method == 'GET':
            return render_template('deletebook.html', title='Delete Book', user=session['user'], role=session['user_role'], book=book)
        elif request.method == 'POST':
            db.session.delete(book)
            db.session.commit()
            return redirect(url_for('section', section_id=section_id))
    else:
        return redirect("/")
    
# request book
@app.route("/book/<book_id>/requestbook", methods=['GET','POST'])
def request_book(book_id):
    book = Book.query.filter_by(id=book_id).first()
    if request.method == 'POST':
        if "user" in session:
            # return render_template('requestbook.html', title='Request Book', user=session['user'], book=book)
            user = User.query.filter_by(username=session['user']).first()
            quota = user.quota
            print(quota)
            book_request = BookRequest.query.filter_by(book_id=book_id, user_id=user.id).first()
            if book_request:
                return redirect(url_for('book', book_id=book_id,  book_request=book_request))
            if quota > 4:
                return redirect(url_for('book', book_id=book_id, quota_error=True))
            book_request = BookRequest(book_id=book.id, user_id=user.id, book_title=book.title, username=user.username)
            db.session.add(book_request)
            user.quota += 1
            db.session.commit()
            return redirect('/')
        else:
            return redirect("/")



# delete book request
@app.route("/book_request/<book_request_id>/delete", methods=['GET','POST'])
def delete_book_request(book_request_id):
    book_request = BookRequest.query.filter_by(id=book_request_id).first()
    if "user" in session:
        user = User.query.filter_by(username=session['user']).first()
        db.session.delete(book_request)
        user.quota -= 1
        db.session.commit()
        return redirect('/')
    else:
        return redirect("/")

# approve book request
@app.route("/book_request/<book_request_id>/approve", methods=['GET','POST'])
def approve_request(book_request_id):
    book_request = BookRequest.query.filter_by(id=book_request_id).first()
    if request.method == 'POST':
        if "user" in session and session['user_role'] == 'admin':
            # username = book_request.username
            # username = str(username).lower()
            # book_title = book_request.book_title
            # book_title = str(book_title).upper()
            # book = Book.query.filter_by(id=book_request.book_id).first()
            # user = User.query.filter_by(id=book_request.user_id).first()
            # book_request.issued = True
            # book_loan = BookLoan(book_id=book.id, user_id=user.id, book_title=book_title, username=username)
            # db.session.add(book_loan)
            # db.session.commit()
            book_request.issued = True
            book_request.date_issued = datetime.date.today()
            book_request.date_due = datetime.date.today() + datetime.timedelta(days=7)
            db.session.commit()
            return redirect(url_for('/', username=session['user']))
        else:
            return redirect("/")
    
# return book
# @app.route("/<book_loan_id>/return", methods=['GET','POST'])