from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from wtform_fields import *
from models import *

# configure app
app = Flask(__name__)
app.secret_key = 'replace later'

# configure database
app.config['SQLALCHEMY_DATABASE_URI'] = ''
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)

@app.route("/", methods = ["GET", "POST"])
def index():
    reg_form = RegistrationForm() # custom form we created

    #* will return TRUE if VALID form was submitted using the POST method
    if reg_form.validate_on_submit():
        username = reg_form.username.data
        password = reg_form.password.data

        hashed_pass = pbkdf2_sha256.hash(password) # automatically takes care of num iterations and adding the 'salt'
    
        user = User(username=username, password=hashed_pass)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('index.html', form=reg_form)


@app.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()

    # Allow user to login if validation success
    if login_form.validate_on_submit():
        return "Logged in!!!"

    # else a get method was used, show them the page!
    return render_template("login.html", form=login_form)


@app.route("/<username>")
def user(username):
    user_obj = User.query.filter_by(username=username).first()
    return str(vars(user_obj))

if __name__ == "__main__":
    app.run(debug=True)