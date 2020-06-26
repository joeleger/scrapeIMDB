import datetime
import os
import pprint

from flask import current_app

from scrapeIMDB import search
import imdb

from scrapeIMDB import create_app
from scrapeIMDB.config import Config
from scrapeIMDB.movies.utils import create_movie

ia = imdb.IMDb()

debug_path = Config.DEBUG_FILE_LOCATION
flat_src = Config.FLAT_FILE_SOURCE
coll_src = Config.COLLECTIONS_FILE_SOURCE


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


def get_rev_files(path_to_source):
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


def get_file_sets(source):
    file_list = []
    for subdir, dirs, files in os.walk(source):
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
    return file_list


def scrape_imdb():
    counter = 0
    file_sources = [coll_src, flat_src]

    try:
        for src in file_sources:
            file_collection = get_rev_files(src)
            for f in file_collection:
                counter += 1
                create_movie(f, counter)

        return "Done"
    except Exception as err:
        print(err)


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


def get_files(source):
    file_list = []
    for file in os.listdir(source):
        if file.endswith(('.mp4', '.webm', '.ogg', '.ogv', '.oga', '.ogx', '.ogm', '.spx', '.opus')):
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


app = create_app()
with app.app_context():
    scrape_imdb()


# sub_dirs = list(folders_in(debug_path))
# if not sub_dirs:
#     print(f'List for {sub_dirs} is empty')
# else:
#     for dir in sub_dirs:
#         print(dir)

# files = get_rev_files(debug_path)
# for file in files:
#     movie_title = str(file['title'])
#     movie_year = int(file['year'])
#     imdb_id = get_movie_id(movie_title, movie_year, 1)
#     movie = get_movie(imdb_id)
#     print(imdb_id)
#     print(movie['title'])
#     print(movie['kind'])


# for file in files:
#     ctr += 1
# print(ctr)

def check_db_title_year():
    source = Config.DEBUG_FILE_LOCATION
    files = get_file_sets(source)
    ctr = 0
    for file in files:
        ctr += 1
        _id = get_movie_id(str(file['title']), int(file['year']), ctr)
        film = get_movie(_id)
        if file['title'].lower() != film['title'].lower().replace(':', '').replace('.', ' '). \
                replace('...', '   ').rstrip():
            print(f'******WARNING**** Movie is potentially missing {file["title"]}')
