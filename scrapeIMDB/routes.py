from flask import render_template, url_for, flash, redirect, request, abort
from flask_login import login_user, current_user, logout_user, login_required
import os
from PIL import Image
import secrets
from scrapeIMDB import app, db, bcrypt
from scrapeIMDB.forms import RegistrationForm, LoginForm, UpdateAccountForm, NewMovieForm
from scrapeIMDB.models import User, Movie
import datetime
import imdb

ia = imdb.IMDb()


@app.route('/')
@app.route('/home')
def home():
    movies = Movie.query.all()
    return render_template('home.html', movies=movies)


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has now been created! You are now able to login.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(f'Login was unsuccessful! Please check email and password.', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash(f'Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@app.route('/movie/new', methods=['GET', 'POST'])
@login_required
def new_movie():
    form = NewMovieForm()
    if form.validate_on_submit():
        movie = Movie(imdb_id=form.imdb_id.data, file_path=form.file_path.data, title=form.title.data,
                      year=form.year.data, genre=form.genre.data, rating=form.rating.data, actors=form.actors.data,
                      directors=form.directors.data, writers=form.writers.data, plot=form.plot.data,
                      runtime=form.runtime.data,
                      poster_url=form.poster_url.data, box_office=form.box_office.data, author=current_user)
        db.session.add(movie)
        db.session.commit()
        flash(f'Your movie has been added!', 'success')
        return redirect(url_for('home'))
    return render_template('create_movie.html', title='New Movie', form=form, legend='Add Movie')


def convert(n):
    return str(datetime.timedelta(seconds=n))


@app.route('/movie/<int:movie_id>')
def movie(movie_id):
    _movie = Movie.query.get_or_404(movie_id)
    running_time = convert(_movie.runtime * 60)
    box_office = '${:,.2f}'.format(_movie.box_office)
    return render_template("movie.html", title=_movie.title, movie=_movie, running_time=running_time,
                           box_office=box_office)


@app.route('/movie/<int:movie_id>/update', methods=['GET', 'POST'])
@login_required
def update_movie(movie_id):
    _movie = Movie.query.get_or_404(movie_id)
    if _movie.author != current_user:
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
        _movie.box_office = form.box_office.data
        db.session.commit()
        flash(f'Your movie has been updated!', 'success')
        return redirect(url_for('movie', movie_id=_movie.id))
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
        form.box_office.data = _movie.box_office
    return render_template('create_movie.html', title='Update Movie',
                           form=form, legend='Update Movie')


@app.route('/movie/<int:movie_id>/delete', methods=['POST'])
@login_required
def delete_movie(movie_id):
    _movie = Movie.query.get_or_404(movie_id)
    if _movie.author != current_user:
        abort(403)
    db.session.delete(_movie)
    db.session.commit()
    flash(f'Your movie is deleted!', 'success')
    return redirect(url_for('home'))


def right(s, amount):
    return s[-amount:]


def mid(s, offset, amount):
    return s[offset:offset + amount]


def get_files(source):
    file_list = []
    for file in os.listdir(source):
        if file.endswith(".mkv") or file.endswith(".mp4") or file.endswith(".avi"):
            file_title = os.path.splitext(file)[0]  # remove the extension
            file_title = file_title.replace(".", " ")  # Remove any periods in text of title
            pos_of_first_brace = len(file_title) - 5
            file_year = mid(file_title, pos_of_first_brace, 4)  # get the year from the file title
            file_path = source + "\\" + file  # get the full file path to launch a video
            file_title = file_title[:-7]  # strip the year and brackets from the end of the title
            file_list.append({'path': file_path,
                              'title': file_title,
                              'year': file_year
                              })
    return file_list


def get_movie_id(title, year):
    try:
        movies = ia.search_movie(title)
        for index, movie in enumerate(movies):
            if str(title.lower()) == movie['title'].lower().replace(':', '') and str(year) == str(movie['year']):
                return movie.movieID
            elif str(title.lower()) == 'Miracle at St  Anna'.lower() and str(year) == str(movie['year']):
                return movie.movieID
            elif str(title.lower()) == 'Mr Church'.lower() and str(year) == str(movie['year']):
                return movie.movieID
            elif str(title.lower()) == 'R I P D '.lower() and str(year) == str(movie['year']):
                return movie.movieID
            elif str(title.lower()) == 'The Man from U N C L E'.lower() and str(year) == str(movie['year']):
                return movie.movieID
            else:
                continue
        return None

    except ia.IMDbError as err:
        print(err)


def get_movie(_id):
    try:
        return ia.get_movie(_id)
    except ia.IMDbError as err:
        print(err)


def create_movie(file):
    try:
        movie_title = str(file['title'])
        movie_year = file['year']
        movie_path = file['path']
        imdb_movie_id = get_movie_id(movie_title, movie_year)
        movie_data = get_movie(imdb_movie_id)
        box_office = movie_data['box office']['Cumulative Worldwide Gross']
        actors_string = ', '.join(map(str, movie_data['cast']))
        directors_string = ', '.join(map(str, movie_data['directors']))
        writers_string = ', '.join(map(str, movie_data['writer']))
        year_converted = int(movie_data['year'])

        _movie = Movie(imdb_id=imdb_movie_id, file_path=movie_path, title=movie_data['title'], year=year_converted,
                       genre=movie_data['genre'], rating=movie_data['rating'], actors=actors_string,
                       directors=directors_string,
                       writers=writers_string, plot=movie_data['plot'], runtime=int(movie_data['runtimes']),
                       poster_url=movie_data['cover url'], box_office=float(box_office), author=current_user)

        db.session.add(_movie)
        db.session.commit()
    except Exception as err:
        print(err)


@app.route('/movie/scrape')
@login_required
def scrape_imdb():
    # Loop through source directory
    # Parse the Title separating the Year
    # get the flat content into a list of dictionaries
    try:
        dir_source = app.config['FLAT_FILE_SOURCE']
        files = get_files(dir_source)
        for file in files:
            create_movie(file)
            return redirect(url_for('home'))
    except Exception as err:
        print(err)
