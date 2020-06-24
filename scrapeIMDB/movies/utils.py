import datetime
import os
import imdb
from flask_login import current_user
from scrapeIMDB import db
from scrapeIMDB.models import Movie

ia = imdb.IMDb()


def convert(n):
    return str(datetime.timedelta(seconds=n))


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


def get_file_sets(source):
    file_list = []
    for subdir, dirs, files in os.walk(source):
        for filename in files:
            file_path = subdir + os.sep + filename
            if file_path.endswith(".mp4") or file_path.endswith(".mkv") or file_path.endswith(".avi"):
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
    return file_list


def get_movie_id(title, year, ctr):
    try:
        print(f'DEBUG -Title - {ctr} - {title}')
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
        print(err)


def get_movie(_id):
    try:
        return ia.get_movie(_id)
    except ia.IMDbError as err:
        print(err)


def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def create_movie(file, counter):
    movie_title = str(file['title'])
    movie_year = file['year']
    movie_path = file['path']
    try:
        imdb_movie_id = get_movie_id(movie_title, movie_year, counter)
        if imdb_movie_id is not None:
            is_added = Movie.get_movie_by_imdb_id(imdb_movie_id)
            if is_added is None:
                imdb_movie_data = get_movie(imdb_movie_id)
                actors_string = ', '.join(map(str, imdb_movie_data['cast']))
                directors_string = ', '.join(map(str, imdb_movie_data['directors']))
                writers_string = ', '.join(map(str, imdb_movie_data['writer']))
                plot_converted = imdb_movie_data['plot'][0]
                genre_string = ', '.join(map(str, imdb_movie_data['genre']))
                year_converted = int(movie_year)
                runtime_converted = int(imdb_movie_data['runtimes'][0])
                movie_item = Movie(imdb_id=imdb_movie_id, file_path=movie_path, title=imdb_movie_data['title'],
                                   year=year_converted, genre=genre_string, rating=imdb_movie_data['rating'],
                                   actors=actors_string, directors=directors_string, writers=writers_string,
                                   plot=plot_converted, runtime=runtime_converted,
                                   poster_url=imdb_movie_data['cover url'],
                                   author=current_user)

                db.session.add(movie_item)
                db.session.commit()
        else:
            return
    except Exception as err:
        db.session.rollback()
        raise
    finally:
        db.session.close()  # optional, depends on use case