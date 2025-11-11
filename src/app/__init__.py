from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from src.utils.config import Config


app = Flask(__name__)

app.config['SECRET_KEY'] = Config._FLASK_SECRET_KEY

app.config['SQLALCHEMY_DATABASE_URI'] = Config._DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bcrypt = Bcrypt(app)
users_database = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Você precisa de uma conta para ver isso.'
login_manager.login_message_category = 'alert-info'

from src.app import routes, users_database


with app.app_context():
    users_database.create_all()