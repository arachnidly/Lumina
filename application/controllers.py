from flask import request, render_template, redirect, url_for, session
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
def login():
    if request.method == 'GET':
        return render_template('login.html', title='User Login')
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        valid_user = User.query.filter_by(username=username).first()
        if valid_user is None:
            return render_template("login.html", username_error=True)
        if valid_user.password != password:
            return render_template('login.html', pwd_error=True)
        is_logged_in = True
        return redirect("/")
    
@app.route("/librarianlogin", methods=['GET', 'POST'])
def librarianlogin():
    if request.method == 'GET':
        return render_template('librarianlogin.html', title='Librarian Login')
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        # valid_user = User.query.filter_by(username=username).first()
        valid_user = User.query.filter_by(username=username, role=1).first()
        if valid_user is None:
            return render_template("librarianlogin.html", username_error=True)
        if valid_user.password != password:
            return render_template('librarianlogin.html', pwd_error=True)
        session['user'] = username
        return redirect("/")
    
# user sign-up page
@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == "GET":
        return render_template('signup.html', title='Sign Up')
    if request.method == 'POST':
        # get form data
        username = request.form['username']
        password = request.form['password']
        password2 = request.form['password2']
        # check if passwords match
        if password != password2:
            return render_template('signup.html', pwd_error = True)
        user = User.query.filter_by(username=username).first()
        if user is not None:
            return render_template('signup.html', username_error=True)
        user = User(username=username, password=password, role=2)
        db.session.add(user)
        db.session.commit()
        session['user'] = username
        return redirect('/')

# logout
@app.route('/logout', methods = ["GET"])
def logout():
    if "user" in session:
        session.pop("user", None)
    return redirect(url_for("home")) 