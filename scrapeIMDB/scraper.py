import os

import imdb
from flask_login import current_user

from scrapeIMDB import db, app
from scrapeIMDB.models import Movie

ia = imdb.IMDb()

dir_source = app.config['FLAT_FILE_SOURCE']


def right(s, amount):
    return s[-amount:]


def mid(s, offset, amount):
    return s[offset:offset + amount]


def check_key(dict, key):
    if key in dict:
        print("Present, ", end=" ")
        print("value =", dict[key])
    else:
        print("Not present")


def get_files(dir_source):
    file_list = []
    for file in os.listdir(dir_source):
        if file.endswith(".mkv") or file.endswith(".mp4") or file.endswith(".avi"):
            file_title = os.path.splitext(file)[0]  # remove the extension
            file_title = file_title.replace(".", " ")  # Remove any periods in text of title
            pos_of_first_brace = len(file_title) - 5
            file_year = mid(file_title, pos_of_first_brace, 4)  # get the year from the file title
            file_path = dir_source + "\\" + file  # get the full file path to launch a video
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
        actors_string = ', '.join(map(str, movie_data['cast']))
        directors_string = ', '.join(map(str, movie_data['directors']))
        writers_string = ', '.join(map(str, movie_data['writer']))
        genre_string = ', '.join(map(str, movie_data['genre']))
        plot_converted = movie_data['plot'][0]
        runtime_converted = int(movie_data['runtimes'][0])
        movie = Movie(imdb_id=imdb_movie_id, file_path=movie_path, title=movie_data['title'],
                      year=int(movie_data['year']),genre=genre_string, rating=movie_data['rating'],
                      actors=actors_string, directors=directors_string, writers=writers_string, plot=plot_converted,
                      runtime=runtime_converted, poster_url=movie_data['cover url'], box_office=None,
                      author=current_user)
        db.session.add(movie)
        db.session.commit()
    except Exception as err:
        print(err)


def process_files():
    # Loop through source directory
    # Parse the Title separating the Year
    # get the flat content into a list of dictionaries

    try:

        files = get_files(dir_source)
        for file in files:
            create_movie(file)
    except Exception as err:
        print(err)


process_files()

# movie_id = get_movie_id('Bloodshot', 2020)
# movie = get_movie(movie_id)
# print(movie['box office'])

# imdb_id = movie_id
# title = movie['title']
# year = movie['year']
# rating = movie['rating']
# casting = movie['cast']
# writer = movie['writer']
# actors = ', '.join(map(str, casting))
# writers = ', '.join(map(str, writer))
# directors = movie['directors']
# directors_string = ', '.join(map(str, directors))
# genre = movie['genres']
# short_plot = movie['plot']
# poster = movie['cover url']
# runtime = movie['runtimes']
# print("******Movie Info*******")
# print(f'{title} - {year}')
# print(f'{rating} - {genre}')
# print(f'Directors: {directors_string}')
# print(f'Actors: {actors}')
# print(f'Poster: {poster}')
# print(f'Plot:  {short_plot}')
# print(f'Runtime: {runtime}')
# print(f'Writers: {writers}')
