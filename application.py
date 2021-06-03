from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy
from wtform_fields import *
from models import *

# configure app
app = Flask(__name__)
app.secret_key = 'replace later'

# configure database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://ifupgnxvqwmwii:cfe31f1cbedadcbfbb4a9d65459f1ffd3de8f330d9dae74d54b4870a59d9db43@ec2-34-195-143-54.compute-1.amazonaws.com:5432/d49m67nj1c58cs'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)

# Configure flask login
login = LoginManager(app)
login.init_app(app)

@login.user_loader
def load_user(id):
    return db.session.query(User).filter(User.id == id).first()

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
        
        flash("Registered Successfully. Please log in.", 'success')
        return redirect(url_for('login'))

    return render_template('index.html', form=reg_form)


@app.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()

    # Allow user to login if validation success
    if login_form.validate_on_submit():
        user_obj = User.query.filter_by(username=login_form.username.data).first()
        login_user(user_obj)

        return redirect(url_for('chat'))

    # else a get method was used, show them the page!
    return render_template("login.html", form=login_form)

@app.route("/chat", methods=["GET", "POST"])
# @login_required
def chat():
    if not current_user.is_authenticated:
        flash("Please log in to view.", 'danger')
        return redirect(url_for('login'))

    return "Chat with me"

@app.route("/logout", methods=["GET"])
def logout():
    logout_user()
    flash("You have logged out successfully", 'success')
    return redirect(url_for('login'))

@app.route("/<username>")
def user(username):
    user_obj = User.query.filter_by(username=username).first()
    if user_obj: return str(vars(user_obj))
    else: return "user not found"


if __name__ == "__main__":
    app.run(debug=True)