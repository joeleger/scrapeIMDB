from os import environ
from dotenv import load_dotenv
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail

load_dotenv('.env')
app = Flask(__name__)
app.config['FLAT_FILE_SOURCE'] = 'F:\\Video\Movies\\_Flat_Structure'
app.config['SECRET_KEY'] = environ.get("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movieListing.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = environ.get('EMAIL_PASS')
mail = Mail(app)
from scrapeIMDB import routes
