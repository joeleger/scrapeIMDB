import os

from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required

from scrapeIMDB import db, create_app
from scrapeIMDB.config import Config
from scrapeIMDB.models import Movie
from scrapeIMDB.movies.forms import NewMovieForm
from scrapeIMDB.movies.utils import convert, get_files, create_movie

movies = Blueprint('movies', __name__)
app = create_app()


@movies.route('/movie/new', methods=['GET', 'POST'])
@login_required
def new_movie():
    form = NewMovieForm()
    if form.validate_on_submit():
        film = Movie(imdb_id=form.imdb_id.data, file_path=form.file_path.data, title=form.title.data,
                     year=form.year.data, genre=form.genre.data, rating=form.rating.data, actors=form.actors.data,
                     directors=form.directors.data, writers=form.writers.data, plot=form.plot.data,
                     runtime=form.runtime.data,
                     poster_url=form.poster_url.data, author=current_user)
        try:
            db.session.add(film)
        except Exception as err:
            app.logger.error(f'Error occurred with adding a new movie - {err}')
        else:
            db.session.commit()
            flash(f'Your movie has been added!', 'success')
            app.logger.debug(f'The movie titled {film.title} was added successfully.')
            return redirect(url_for('main.home'))
    return render_template('create_movie.html', title='New Movie', form=form, legend='Add Movie')


@movies.route('/movie/<int:movie_id>')
def movie(movie_id):
    _movie = Movie.query.get_or_404(movie_id)
    running_time = convert(_movie.runtime * 60)
    actor_list = _movie.actors.split(',')
    actors = ', '.join(map(str, actor_list[0:11]))

    return render_template("movie.html", title=_movie.title, movie=_movie, running_time=running_time,
                           actors=actors)


@movies.route('/movie/<int:movie_id>/update', methods=['GET', 'POST'])
@login_required
def update_movie(movie_id):
    _movie = Movie.query.get_or_404(movie_id)
    if _movie.author != current_user:
        app.logger.warning(f'The user {current_user} is not authenticated to update this film.')
        abort(403)
    form = NewMovieForm()
    if form.validate_on_submit():
        _movie.imdb_id = form.imdb_id.data
        _movie.file_path = form.file_path.data
        _movie.title = form.title.data
        _movie.year = form.year.data
        _movie.genre = form.genre.data
        _movie.rating = form.rating.data
        _movie.actors = form.actors.data
        _movie.directors = form.directors.data
        _movie.writers = form.writers.data
        _movie.plot = form.plot.data
        _movie.runtime = form.runtime.data
        _movie.poster_url = form.poster_url.data
        db.session.commit()
        flash(f'Your movie has been updated!', 'success')
        app.logger.debug(f'The movie titled {_movie.title} was updated successfully.')
        return redirect(url_for('movies.movie', movie_id=_movie.id))
    elif request.method == 'GET':
        form.imdb_id.data = _movie.imdb_id
        form.file_path.data = _movie.file_path
        form.title.data = _movie.title
        form.year.data = _movie.year
        form.genre.data = _movie.genre
        form.rating.data = _movie.rating
        form.actors.data = _movie.actors
        form.directors.data = _movie.directors
        form.writers.data = _movie.writers
        form.plot.data = _movie.plot
        form.runtime.data = _movie.runtime
        form.poster_url.data = _movie.poster_url
    return render_template('create_movie.html', title='Update Movie',
                           form=form, legend='Update Movie')


@movies.route('/movie/<int:movie_id>/delete', methods=['POST'])
@login_required
def delete_movie(movie_id):
    _movie = Movie.query.get_or_404(movie_id)
    if _movie.author != current_user:
        abort(403)
    file = _movie.file_path
    try:
        os.remove(file)
        db.session.delete(_movie)
        db.session.commit()
        flash(f'Your movie is deleted!', 'success')
        app.logger.debug(f'The movie, {_movie.title} was deleted successfully!')
    except OSError as e:
        flash(f'Error: {e.filename} - {e.strerror}', 'danger')
        # remove the db record even if the file does not exist in file system
        app.logger.error(
            f'The movie titled,"{_movie.title}" was deleted successfully however the file does not exist')
        db.session.delete(_movie)
        db.session.commit()
        flash(f'Your movie is deleted!', 'success')
    finally:
        return redirect(url_for('main.home'))


@movies.route('/movie/scrape')
@login_required
def scrape_imdb():
    counter = 0
    # TODO: create a Configuration model for this and other configurable types then obtain this
    #  from db instead of hardcoded
    file_sources = [Config.FLAT_FILE_SOURCE, Config.COLLECTIONS_FILE_SOURCE]
    try:
        app.logger.debug(f'Starting IMDB scrape.')
        for src in file_sources:
            file_collection = get_files(src)
            for f in file_collection:
                # counter += 1
                create_movie(f, app)
        app.logger.debug(f'Ending IMDB scrape.')
        return redirect(url_for('main.home'))
    except Exception as err:
        app.logger.error(f'Scraping Movie folder resulted in an error - {err}')


@movies.route('/movie/player/<int:movie_id>')
def movie_player(movie_id):
    _movie = Movie.query.get_or_404(movie_id)

    return render_template('movie_player.html', movie=_movie, title=_movie.title, )
