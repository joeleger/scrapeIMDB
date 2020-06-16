from datetime import datetime
from scrapeIMDB import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    movies = db.relationship('Movie', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    imdb_id = db.Column(db.String(50), unique=True, nullable=False)
    file_path = db.Column(db.String(300), nullable=False)
    title = db.Column(db.String(500), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    actors = db.Column(db.Text, nullable=False)
    directors = db.Column(db.String(300), nullable=False)
    writers = db.Column(db.String(500), nullable=False)
    plot = db.Column(db.Text, nullable=False)
    runtime = db.Column(db.Integer, nullable=False)
    poster_url = db.Column(db.String(500), nullable=False)
    box_office = db.Column(db.Float, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    last_updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    @staticmethod
    def get_movie_by_title_year(title, year):
        query = Movie.query.filter(Movie.title == title, Movie.year == year).first()
        if query is None:
            return None
        else:
            return query

    @staticmethod
    def get_movie_by_imdb_id(imdb_id):
        query = Movie.query.filter(Movie.imdb_id == imdb_id).first()
        if query is None:
            return None
        else:
            return query

    def __repr__(self):
        return f"Movie('{self.title}', '{self.year}', '{self.last_updated}')"
