from time import localtime, strftime
from flask import Flask, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from wtform_fields import *
from models import *

# configure app
app = Flask(__name__)
app.secret_key = 'replace later'

# configure database
app.config['SQLALCHEMY_DATABASE_URI'] = ''
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)

# Initialize flask Socketio
socketio = SocketIO(app)
ROOMS = ["lounge", "news", "games", "coding"]

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
    # if not current_user.is_authenticated:
    #     flash("Please log in to view.", 'danger')
    #     return redirect(url_for('login'))

    return render_template('chat.html', username=current_user.username, rooms=ROOMS)

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


@socketio.on('message')
def message(data):
    print(f"\n\n{data}\n\n")
    # sends that data to connected clients -- by default, it pushes it to the event bucket called 'message'
    send({
        'msg':data['msg'], 
        'username':data['username'], 
        'time_stamp': strftime('%b-%d %I:%M%p', localtime())
    }, room=data['room']) 
    # emit('some-event', 'this is a custom event message') # sends data to the 'some-event' bucket on clientside

@socketio.on('join')
def join(data):
    join_room(data['room'])
    send({'msg': data['username'] + ' has joined the room ' + data['room']}, room=data['room'] )

@socketio.on('leave')
def leave(data):
    leave_room(data['room'])
    send({'msg': data['username'] + ' has left the room ' + data['room']}, room=data['room'] )

if __name__ == "__main__":
    # app.run(debug=True)  
    socketio.run(app, debug=True)