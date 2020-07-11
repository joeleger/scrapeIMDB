import datetime
import os
import imdb
from flask import current_app
from flask_login import current_user
from scrapeIMDB import db, Config
from scrapeIMDB.models import Movie
import traceback
from werkzeug.utils import secure_filename


ia = imdb.IMDb()


def convert(n):
    return str(datetime.timedelta(seconds=n))


def right(s, amount):
    return s[-amount:]


def mid(s, offset, amount):
    return s[offset:offset + amount]


def folders_in(path_to_parent):
    for full_name in os.listdir(path_to_parent):
        if os.path.isdir(os.path.join(path_to_parent, full_name)):
            yield os.path.join(path_to_parent, full_name)


def get_movie_file_path_list(_file):
    file_list = []
    file_title = os.path.splitext(_file)[0]  # remove the extension
    file_title = file_title.replace(".", " ")  # Remove any periods in text of title
    pos_of_first_brace = len(file_title) - 5
    file_year = mid(file_title, pos_of_first_brace, 4)  # get the year from the file title
    file_path = Config.FLAT_FILE_SOURCE + "\\" + _file  # get the full file path to launch a video
    file_title = file_title[:-7]  # strip the year and brackets from the end of the title
    file_list.append({'path': file_path,
                      'title': file_title,
                      'year': file_year
                      })
    return file_list


def get_files(path_to_source):
    file_list = []
    contains_sub_dirs = folders_in(path_to_source)
    if contains_sub_dirs:
        for subdir, dirs, files in os.walk(path_to_source):
            for filename in files:
                file_path = subdir + os.sep + filename
                if file_path.endswith(('.mp4', '.webm', '.ogg', '.ogv', '.oga', '.ogx', '.ogm', '.spx', '.opus')):
                    file_title = os.path.splitext(filename)[0]  # remove the extension
                    file_title = file_title.replace(".", " ")  # Remove any periods in text of title
                    pos_of_first_brace = len(file_title) - 5
                    file_year = mid(file_title, pos_of_first_brace, 4)  # get the year from the file title
                    file_path = subdir + "\\" + filename  # get the full file path to launch a video
                    file_title = file_title[:-7]  # strip the year and brackets from the end of the title
                    file_list.append({'path': file_path,
                                      'title': file_title,
                                      'year': file_year
                                      })
    else:  # no sub directories
        for f in os.listdir(path_to_source):
            if f.endswith(('.mp4', '.webm', '.ogg', '.ogv', '.oga', '.ogx', '.ogm', '.spx', '.opus')):
                file_title = os.path.splitext(f)[0]  # remove the extension
                file_title = file_title.replace(".", " ")  # Remove any periods in text of title
                pos_of_first_brace = len(file_title) - 5
                file_year = mid(file_title, pos_of_first_brace, 4)  # get the year from the file title
                file_path = path_to_source + "\\" + f  # get the full file path to launch a video
                file_title = file_title[:-7]  # strip the year and brackets from the end of the title
                file_list.append({'path': file_path,
                                  'title': file_title,
                                  'year': file_year
                                  })
    return file_list


def get_movie_id(title, year, app):
    try:
        # app.logger.debug(f' {ctr} - {title}')
        movies = ia.search_movie(title)
        for index, film in enumerate(movies):
            if str(title.lower()).rstrip() == film['title'].lower().replace(':', '').replace('.', ' '). \
                    replace('...', '  ').rstrip() \
                    and str(year) == str(film['year']) \
                    and film['kind'].lower() == 'movie' \
                    or film['kind'].lower() == 'tv movie' \
                    or film['kind'].lower() == 'video movie':
                return film.movieID
            else:
                continue
        return None

    except ia.IMDbError as err:
        app.logger.error(''.join(traceback.format_exception(etype=type(err), value=err, tb=err.__traceback__)))
        # app.logger.error(f'Error in get movie id - {err}')


def get_movie(_id, app):
    try:
        return ia.get_movie(_id)
    except ia.IMDbError as err:
        app.logger.error(''.join(traceback.format_exception(etype=type(err), value=err, tb=err.__traceback__)))


def create_movie(file, app, using_uploader, form_file_field):
    movie_title = str(file['title'])
    movie_year = file['year']
    movie_path = file['path']
    app.logger.debug(f'movie path = {movie_path}')
    try:
        imdb_movie_id = get_movie_id(movie_title, movie_year, app)
        app.logger.debug(f'IMDBID -> {imdb_movie_id}')
        if imdb_movie_id is not None:
            is_added = Movie.get_movie_by_imdb_id(imdb_movie_id)
            app.logger.debug(f'is_added -> {is_added}')
            if is_added is None:
                try:
                    imdb_movie_data = get_movie(imdb_movie_id, app)
                    app.logger.debug(f'is_added -> {imdb_movie_data}')
                    actors_string = ', '.join(map(str, imdb_movie_data['cast']))
                    app.logger.debug(f'Actors -> {actors_string}')
                    directors_string = ', '.join(map(str, imdb_movie_data['directors']))
                    app.logger.debug(f'Directors -> {directors_string}')
                    writers_string = ', '.join(map(str, imdb_movie_data['writer']))
                    app.logger.debug(f'Writers -> {writers_string}')
                    plot_converted = imdb_movie_data['plot'][0]
                    app.logger.debug(f'Plot -> {plot_converted}')
                    genre_string = ', '.join(map(str, imdb_movie_data['genre']))
                    app.logger.debug(f'Genre -> {genre_string}')
                    year_converted = int(movie_year)
                    app.logger.debug(f'Year -> {year_converted}')
                    runtime_converted = int(imdb_movie_data['runtimes'][0])
                    app.logger.debug(f'Runtime -> {runtime_converted}')
                    movie_item = Movie(imdb_id=imdb_movie_id, file_path=movie_path, title=imdb_movie_data['title'],
                                       year=year_converted, genre=genre_string, rating=imdb_movie_data['rating'],
                                       actors=actors_string, directors=directors_string, writers=writers_string,
                                       plot=plot_converted, runtime=runtime_converted,
                                       poster_url=imdb_movie_data['cover url'],
                                       author=current_user)
                    app.logger.debug(f'Movie Item before adding -> {movie_item}')
                    db.session.add(movie_item)
                except Exception as err:
                    app.logger.error(''.join(traceback.format_exception(etype=type(err), value=err, tb=err.__traceback__)))
                    db.session.rollback()
                    raise
                else:
                    db.session.commit()
                    if using_uploader:
                        movie_fn = save_movie_file(form_file_field, app)
                        app.logger.debug(f'Movie Path directory is - {movie_fn}.')

                    return True
                finally:
                    db.session.close()
            else:
                return False
    except Exception as err:
        app.logger.error(''.join(traceback.format_exception(etype=type(err), value=err, tb=err.__traceback__)))
        db.session.rollback()
        raise
    finally:
        db.session.close()


def delete_upload_source(movie_fn, app):
    try:
        file_path = os.path.join(Config.UPLOAD_MOVIE_SOURCE, movie_fn)
        os.remove(file_path)
        return True
    except OSError as e:
        app.logger.error(''.join(traceback.format_exception(etype=type(e), value=e, tb=e.__traceback__)))
        return False


def save_movie_file(form_movie_data, app):
    movie_fn = secure_filename(form_movie_data.filename)
    movie_file_path = os.path.join(Config.FLAT_FILE_SOURCE, movie_fn)
    try:
        # save movie to destination source
        form_movie_data.save(movie_file_path)
    except Exception as err:
        app.logger.error(''.join(traceback.format_exception(etype=type(err), value=err, tb=err.__traceback__)))

    return movie_fn
