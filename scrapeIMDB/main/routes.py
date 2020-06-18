from flask import render_template, request, Blueprint
from scrapeIMDB.models import Movie

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    page = request.args.get('page', 1, type=int)
    movies = Movie.query.order_by(Movie.rating.desc(), Movie.title.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', movies=movies)


@main.route('/about')
def about():
    return render_template('about.html', title='About')
