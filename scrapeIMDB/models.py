from datetime import datetime
from scrapeIMDB import db


class User(db.Model):
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
    imdb_id = db.Column(db.String(50), nullable=False)
    file_path = db.Column(db.String(300), nullable=False)
    title = db.Column(db.String(500), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    actors = db.Column(db.String(5000), nullable=False)
    directors = db.Column(db.String(300), nullable=False)
    writers = db.Column(db.String(300), nullable=False)
    plot = db.Column(db.Text, nullable=False)
    runtime = db.Column(db.Integer, nullable=False)
    poster_url = db.Column(db.String(500), nullable=False)
    box_office = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    last_updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, _imdb_id, _file_path, _title, _year,
                 _genre, _rating, _actors, _directors, _writers,
                 _plot, _runtime, _poster_url, _box_office, _user_id):
        self.imdb_id = _imdb_id
        self.file_path = _file_path
        self.title = _title
        self.year = _year
        self.genre = _genre
        self.rating = _rating
        self.actors = _actors
        self.directors = _directors
        self.writers = _writers
        self.plot = _plot
        self.runtime = _runtime
        self.poster_url = _poster_url
        self.box_office = _box_office
        self.user_id = _user_id

    def __repr__(self):
        return f"Movie('{self.title}', '{self.year}', '{self.last_updated}')"