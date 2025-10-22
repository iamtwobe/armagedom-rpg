from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from src.utils.secret_key_handler import read_secret_key
from src.utils.db_url_handler import read_db_url
import os


app = Flask(__name__)

app.config['SECRET_KEY'] = read_secret_key(".env")

app.config['SQLALCHEMY_DATABASE_URI'] = read_db_url(".env")
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