from flask import request, render_template, redirect, url_for, session
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required
from flask import current_app as app
from application.models import *
from application.config import *

# home page
@app.route('/', methods=['GET', 'POST'])
@app.route("/home")
def home():
    # if user isn't logged in, redirect to welcome page with login button
    if "user" in session:
        return render_template('home.html', title='Home')
    else:
        return render_template('welcome.html', title='Welcome')
    
@app.route("/login", methods=['GET', 'POST'])
@app.route("/librarianlogin", methods=['GET', 'POST'])
def login():
    lib = False  # Define and initialize the 'lib' variable as False
    if request.path == "/librarianlogin":  # Check if the route clicked is '/librarianlogin'
        lib = True  # Set 'lib' to True if the route is '/librarianlogin'
        pagetitle = "Librarian Login"  # Set the page title to 'Librarian Login'
    elif request.path == "/login":  # Check if the route clicked is '/login'
        pagetitle = "Login"  # Set the page title to 'Login'
    
    if 'user' in session:
        return redirect("/")
    else:
        if request.method == 'GET':
            return render_template('login.html', title=pagetitle, lib=lib)  # Render the template with the 'lib' value
        if request.method == 'POST':
            username = request.form["username"].lower()
            password = request.form["password"]
            valid_user = User.query.filter_by(username=username).first()
            if valid_user is None:
                return render_template("login.html", username_error=True, title=pagetitle, lib=lib)
            if valid_user.password != password:
                return render_template('login.html', pwd_error=True, title=pagetitle, lib=lib)
            session['user'] = username
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
            return redirect("/")



# logout
@app.route('/logout', methods = ["GET"])
def logout():
    if "user" in session:
        session.pop("user", None)
    return redirect(url_for("home")) 


