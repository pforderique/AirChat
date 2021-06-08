from flask import Flask
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv
from os import environ, path

# take environment variables from .env
load_dotenv()

# global variables
DB_NAME = 'maindb.db'
db = SQLAlchemy()
socketio = SocketIO()
login = LoginManager()

def create_app():

    # configure app
    app = Flask(__name__)
    app.secret_key = environ.get("SECRET_KEY")
    app.config['WTF_CSRF_SECRET_KEY'] = environ.get('CSRF_SECRET_KEY')

    # configure database
    app.config['SQLALCHEMY_DATABASE_URI'] =  environ.get("DB_URI") #f'sqlite:///{DB_NAME}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    from .views import views
    from .auth import auth
    from . import sockets
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    # Initalize the database
    db.init_app(app)
    # create_database(app)
    db.create_all(app=app)

    # Initialize flask Socketio
    socketio.init_app(app)

    # Configure flask login
    login.init_app(app)

    return app


def create_database(app:Flask):
    # create only it it doesnt exist yet
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print("Database created!")