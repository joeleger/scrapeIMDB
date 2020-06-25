from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from scrapeIMDB import db, login_manager
from flask_login import UserMixin
from scrapeIMDB.search import add_to_index, remove_from_index, query_index


class SearchableMixin(object):
    @classmethod
    def search(cls, expression, page, per_page):
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(db.case(when, value=cls.id)), total

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)


db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)


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

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config["SECRET_KEY"], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Movie(SearchableMixin, db.Model):
    __searchable__ = ['title', 'plot']

    id = db.Column(db.Integer, primary_key=True)
    imdb_id = db.Column(db.String(50), unique=True, nullable=False)
    file_path = db.Column(db.String(2000), nullable=False)
    title = db.Column(db.String(500), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String(300), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    actors = db.Column(db.Text, nullable=False)
    directors = db.Column(db.String(300), nullable=False)
    writers = db.Column(db.String(500), nullable=False)
    plot = db.Column(db.Text, nullable=False)
    runtime = db.Column(db.Integer, nullable=False)
    poster_url = db.Column(db.String(1000), nullable=False)
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
