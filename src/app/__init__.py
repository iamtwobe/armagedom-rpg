from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from src.utils.secret_key_handler import read_secret_key
from src.utils.db_url_handler import read_db_url
from src.utils.config import Config


app = Flask(__name__)

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

app.config['SECRET_KEY'] = Config._FLASK_SECRET_KEY

app.config['SQLALCHEMY_DATABASE_URI'] = Config._DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bcrypt = Bcrypt(app)
users_database = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Você precisa de uma conta para ver isso.'
login_manager.login_message_category = 'alert-info'

from src.app import routes, users_database, admin_routes

app.register_blueprint(admin_bp)

with app.app_context():
    users_database.create_all()