from flask import Flask, request, redirect, url_for
from flask import render_template

# create app instance
app = Flask(__name__)

# home page
@app.route("/")
@app.route("/home")
def home():
    # if user isn't logged in, redirect to welcome page
    return render_template('welcome.html')

    # if user is logged in, redirect to user dashboard page
    return render_template('index.html')

# user login page


# librarian login page


# user register page


# general user profile page


# librarian dashboard




# app run   
if __name__ == "__main__":
    app.run(
        host='0.0.0.0',
        debug=True,
        port=8080
    )

