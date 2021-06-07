from flask_login import UserMixin
from datetime import datetime
from . import db

# table for many to many relationships
chats = db.Table('chats',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('room_id', db.Integer, db.ForeignKey('rooms.id'), primary_key=True)
)

# admins = db.Table('admins',
#     db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
#     db.Column('room_id', db.Integer, db.ForeignKey('room.id'), primary_key=True)
# )

class User(UserMixin, db.Model):
    """ User Model """

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    date_joined = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    rooms = db.relationship('Room', secondary=chats, backref=db.backref('participants'), lazy=True) 

class Room(db.Model):
    """ Room Model """

    __tablename__ = 'rooms'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)