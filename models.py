from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
# from application import app

db = SQLAlchemy()
# db.init_app(app=app)

class User(
    UserMixin, 
    db.Model):
    """ User Model """

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)


# # ! RUN ONCE ONLY -- THIS WORKS! Just uncomment this and db.init_app
# db.create_all(app=app)