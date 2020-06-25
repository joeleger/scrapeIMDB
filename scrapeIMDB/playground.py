import datetime
import os
import pprint
from scrapeIMDB import search
import imdb

from scrapeIMDB import create_app
from scrapeIMDB.config import Config
from scrapeIMDB.models import Movie

ia = imdb.IMDb()

path = Config.COLLECTIONS_FILE_SOURCE


def convert(n):
    return str(datetime.timedelta(seconds=n))


def right(s, amount):
    return s[-amount:]


def mid(s, offset, amount):
    return s[offset:offset + amount]


def get_file_sets(source):
    file_list = []
    for subdir, dirs, files in os.walk(source):
        for filename in files:
            file_path = subdir + os.sep + filename
            if file_path.endswith(".mp4") or file_path.endswith(".webm") or file_path.endswith(".ogg"):
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
        print(f'DEBUG - {ctr}')
        movies = ia.search_movie(title)
        for index, film in enumerate(movies):
            if str(title.lower()).rstrip() == film['title'].lower().replace(':', '') \
                    and str(year) == str(film['year']) \
                    and film['kind'].lower() == 'movie' or film['kind'].lower() == 'tv movie' \
                    or film['kind'].lower() == 'video movie':
                return film.movieID
            elif str(title.lower()) == 'Miracle at St  Anna'.lower() and str(year) == str(film['year']) \
                    and film['kind'].lower() == 'movie':
                return film.movieID
            elif str(title.lower()) == 'Mr Church'.lower() and str(year) == str(film['year']) \
                    and film['kind'].lower() == 'movie':
                return film.movieID
            elif str(title.lower()) == 'R I P D '.lower() and str(year) == str(film['year']) \
                    and film['kind'].lower() == 'movie':
                return film.movieID
            elif str(title.lower()) == 'The Man from U N C L E'.lower() and str(year) == str(film['year']) \
                    and film['kind'].lower() == 'movie':
                return film.movieID
            elif str(title.lower()) == 'Guardians of the Galaxy Vol  2'.lower() and str(year) == str(film['year']) \
                    and film['kind'].lower() == 'movie':
                return film.movieID
            elif str(title.lower()) == 'G I  Joe Retaliation'.lower() and str(year) == str(film['year']) \
                    and film['kind'].lower() == 'movie':
                return film.movieID
            elif str(title.lower()) == 'G I  Joe The Rise of Cobra'.lower() and str(year) == str(film['year']) \
                    and film['kind'].lower() == 'movie':
                return film.movieID
            elif str(title.lower()) == 'A I  Artificial Intelligence'.lower() and str(year) == str(film['year']) \
                    and film['kind'].lower() == 'movie':
                return film.movieID
            elif str(title.lower()) == 'Once Upon a Time in Hollywood'.lower() and str(year) == str(film['year']) \
                    and film['kind'].lower() == 'movie':
                return film.movieID
            elif str(title.lower()) == 'Batman V Superman Dawn Of Justice'.lower() and str(year) == str(film['year']) \
                    and film['kind'].lower() == 'movie':
                return film.movieID
            elif str(title.lower()) == 'Dr  Strangelove or How I Learned to Stop Worrying and Love the Bomb'.lower() \
                    and str(year) == str(film['year']) and film['kind'].lower() == 'movie':
                return film.movieID
            elif str(title.lower()) == 'Dr  No'.lower() \
                    and str(year) == str(film['year']) and film['kind'].lower() == 'movie':
                return film.movieID
            else:
                continue
        return None

    except ia.IMDbError as err:
        print(err)


def get_rev_movie_id(title, year, ctr):
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


def get_movie_advanced(_id):
    try:
        return ia.search_movie_advanced(_id)
    except ia.IMDbError as err:
        print(err)


# title = "Once Upon a Time... in Hollywood"
# title = title.replace('.', ' ').rstrip()
#
# pp = pprint.PrettyPrinter(width=80, compact=False)
# # # 1583421
# imdb_id = get_movie_id(title, 2019, 1)
# movie = get_movie_advanced(imdb_id)
# print(imdb_id)

# print(movie['title'])
# print(movie['kind'])
# for m in movie:
#     pp.pprint(m)


# ctr = 0


# for file in files:
#     ctr += 1
# print(ctr)

def check_db_title_year():
    source = Config.DEBUG_FILE_LOCATION
    files = get_file_sets(source)
    ctr = 0
    for file in files:
        ctr += 1
        _id = get_rev_movie_id(str(file['title']), int(file['year']), ctr)
        film = get_movie(_id)
        if file['title'].lower() != film['title'].lower().replace(':', '').replace('.', ' '). \
                replace('...', '   ').rstrip():
            print(f'******WARNING**** Movie is potentially missing {file["title"]}')


app = create_app()
with app.app_context():
    Movie.reindex()
    # app.elasticsearch.indices.delete('movie')
    query, total = Movie.search('gangster', 1, 5)
    print(total)
    print(query.all())
