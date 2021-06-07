from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, login_required, logout_user
from .wtform_fields import *
from .models import User, Room
from . import db

views = Blueprint('views', __name__)

@views.route("/", methods = ["GET", "POST"])
def home():
    return redirect(url_for('auth.signup'))


@views.route("/chat", methods=["GET", "POST"])
# @login_required
def chat():
    if request.method == "GET":
        if not current_user.is_authenticated:
            flash("Please log in to view.", 'danger')
            return redirect(url_for('auth.login'))

        current_room = "Global"

    if request.method == "POST":
        room_name = request.form.get("room_name")
        password = request.form.get("password")

        print(f"got room {room_name} with pass {password}")
        
        room = db.session.query(Room).filter_by(name=room_name).first()
        # if room name already exists, sign into this room (aka add user as participant)
        if room:
            if pbkdf2_sha256.verify(password, room.password):
                room.participants.append(current_user)
                db.session.commit()
                flash('Signed into room', 'success')
            else:
                flash('Password incorrect', 'danger')

        # else create this room for the user (add them as participant)
        else:
            hashed_pass = pbkdf2_sha256.hash(password)
            room = Room(name=room_name, password=hashed_pass)
            current_user.rooms.append(room)
            db.session.commit()
            flash("room created successfully", 'success')

        current_room = room.name

    # pass in the user's rooms in order of (most recent ... less recent)
    rooms = reversed(list(current_user.rooms)) 

    return render_template('chat.html', user=current_user, rooms=rooms, current_room=current_room)

@views.route("/<username>")
def user(username):
    user_obj = User.query.filter_by(username=username).first()
    if user_obj: return str(vars(user_obj))
    else: return "user not found"