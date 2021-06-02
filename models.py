from flask_sqlalchemy import SQLAlchemy
from application import app

db = SQLAlchemy()
# db.init_app(app=app)

class User(db.Model):
    """ User Model """

    __tablename__ = "users"
    _id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)


# # ! RUN ONCE ONLY
# db.create_all(app=app)