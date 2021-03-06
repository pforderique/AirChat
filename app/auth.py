from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, current_user, login_required, logout_user
from .models import User
from .wtform_fields import *
from . import login, db

auth = Blueprint('auth', __name__)

@login.user_loader
def load_user(id):
    return db.session.query(User).filter(User.id == id).first()

@auth.route("/signup", methods = ["GET", "POST"])
def signup():
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
        return redirect(url_for('auth.login'))

    return render_template('index.html', form=reg_form)

@auth.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()

    # Allow user to login if validation success
    if login_form.validate_on_submit():
        user_obj = User.query.filter_by(username=login_form.username.data).first()
        login_user(user_obj)

        return redirect(url_for('views.chat'))

    # else a get method was used, show them the page!
    return render_template("login.html", form=login_form)

@auth.route("/logout", methods=["GET"])
def logout():
    logout_user()
    flash("You have logged out successfully", 'success')
    return redirect(url_for('auth.login'))
