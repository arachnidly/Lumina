from flask import Flask, request, redirect, url_for
from flask import render_template

# create app instance
app = Flask(__name__)

# home page if user is not logged in
@app.route("/")
@app.route("/home")
def index():
    ishome = True
    return render_template('index.html', ishome=ishome, title='Home')

# user login page
@app.route("/userlogin", methods=['GET', 'POST'])
def userlogin():
    return render_template('userlogin.html', title='User Login')

# librarian login page
@app.route("/librarianlogin", methods=['GET', 'POST'])
def librarianlogin():
    return render_template('librarianlogin.html', title='Librarian Login')

# user register page
@app.route("/userregister", methods=['GET', 'POST'])
def userregister():
    return render_template('userregister.html', title='User Register')

# general user profile page
@app.route("/userprofile", methods=['GET', 'POST'])
def userprofile():
    if request.method == 'POST':
        isloggedin = True
        user = request.form['user']
        return render_template('userprofile.html' , username=user, title=f"{user}'s Profile", isloggedin=isloggedin)


# librarian dashboard
@app.route("/librariandashboard", methods=['GET', 'POST'])
def librariandashboard():
    if request.method == 'POST':
        isloggedin = True
        admin = request.form['name']
        return render_template('librariandashboard.html', admin = admin, title="Librarian Dashboard", isloggedin=isloggedin)

@app.route("/logout")
def logout():
    return redirect(url_for('index'))

# Test Page - Delete Later
@app.route("/test", methods=['GET', 'POST'])
def test():
    return render_template('test.html')


# app run   
if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        debug=True,
        port=8080
    )

