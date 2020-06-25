from dotenv import load_dotenv
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from scrapeIMDB.config import Config
from elasticsearch import Elasticsearch


load_dotenv('.env')

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    app.elasticsearch = Elasticsearch(Config.ELASTICSEARCH_URL, timeout=30) \
        if Config.ELASTICSEARCH_URL else None

    from scrapeIMDB.users.routes import users
    from scrapeIMDB.movies.routes import movies
    from scrapeIMDB.main.routes import main
    from scrapeIMDB.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(movies)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app
