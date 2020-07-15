from flask import render_template, request, Blueprint, g, redirect, url_for, session
from scrapeIMDB.models import Movie
from scrapeIMDB.movies.forms import SearchForm
from scrapeIMDB.config import Config
from scrapeIMDB.movies.utils import delete_upload_source
from scrapeIMDB import create_app

main = Blueprint('main', __name__)
app = create_app()


@main.before_app_request
def before_request():
    g.search_form = SearchForm()


@main.route('/')
@main.route('/home')
def home():
    file = request.args.get('file')
    if file:
        # delete needs to occur from result of redirect from create New Movie
        app.logger.debug(f'File to delete {file}')
        delete_upload_source(file, app)
        session.pop('FileName', None)

    page = request.args.get('page', 1, type=int)
    movies = Movie.query.order_by(Movie.rating.desc(), Movie.title.desc()).paginate(page=page, per_page=10)
    # movies = Movie.query.order_by(Movie.title.asc()).paginate(page=page, per_page=100)
    return render_template('home.html', movies=movies)


@main.route('/about')
def about():
    return render_template('about.html', title='About')


@main.route('/search')
def search():
    if not g.search_form.validate():
        return redirect(url_for('main.home'))
    page = request.args.get('page', 1, type=int)
    movies, total = Movie.search(g.search_form.q.data, page,
                                 Config.MOVES_PER_PAGE)
    next_url = url_for('main.search', q=g.search_form.q.data, page=page + 1) \
        if total > page * Config.MOVES_PER_PAGE else None
    prev_url = url_for('main.search', q=g.search_form.q.data, page=page - 1) \
        if page > 1 else None
    return render_template('search.html', title='Search', movies=movies,
                           next_url=next_url, prev_url=prev_url)
