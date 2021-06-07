from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, current_user, login_required, logout_user
from .models import User
from . import db

views = Blueprint('views', __name__)
ROOMS = ["lounge", "news", "games", "coding"]

@views.route("/", methods = ["GET", "POST"])
def home():
    return redirect(url_for('auth.signup'))


@views.route("/chat", methods=["GET", "POST"])
# @login_required
def chat():
    if not current_user.is_authenticated:
        flash("Please log in to view.", 'danger')
        return redirect(url_for('auth.login'))

    return render_template('chat.html', username=current_user.username, rooms=ROOMS)

@views.route("/<username>")
def user(username):
    user_obj = User.query.filter_by(username=username).first()
    if user_obj: return str(vars(user_obj))
    else: return "user not found"