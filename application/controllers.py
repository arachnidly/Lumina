from flask import request, render_template, redirect, url_for, session
from flask_security import Security, UserMixin, RoleMixin, login_required, roles_required
from flask import current_app as app
from application.models import *
from application.config import *

# home page
@app.route('/', methods=['GET', 'POST'])
@app.route("/home")
def home():
    # if user isn't logged in, redirect to welcome page with login button
    if "user" in session:
        role = session['user_role']
        # return redirect("/user=" + session["user"])
        if role == 'admin':
            return render_template('librariandashboard.html', title='Librarian Dashboard', role=role, user=session['user'])
        else:
            return render_template('userdashboard.html', title='Dashboard', role=role, user=session['user'])
    else:
        return render_template('welcome.html', title='Welcome')
    
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
    if "user" in session and session['user'] == username:
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
        if request.method == 'GET':
            return render_template('search.html', title='Search', user=session['user'], role=session['user_role'])
        if request.method == 'POST':
            search_term = request.form['search']
            # books = Book.query.filter(Book.title.ilike(f'%{search_term}%')).all()
            # return render_template('search.html', title='Search', books=books)
            return render_template('search.html', title='Search', user=session['user'], role=session['user_role'], search_term=search_term)
    else:
        return redirect("/")
    
# manage
@app.route("/manage")
def manage():
    if "user" in session and session['user_role'] == 'admin':
        if request.method == 'GET':
            # get all sections
            sections = Section.query.all()
            
            return render_template('manage.html', title='Manage', user=session['user'], role=session['user_role'])
        else:
            redirect("/manage/")
    else:
        return redirect("/")


# add section
@app.route("/addsection", methods=['GET', 'POST'])
def add_section():
    if request.method == 'GET':
        if "user" in session and session['user_role'] == 'admin':
                # sections = Section.query.all()
                return render_template('addsection.html', title='Add Section', user='athena', role='admin', sections=sections) 
        return redirect("/")

