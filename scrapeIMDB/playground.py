import imdb

from scrapeIMDB.config import Config
from scrapeIMDB.movies.utils import get_movie_id, get_movie, get_movie_file_path_list, get_files

ia = imdb.IMDb()

debug_path = Config.DEBUG_FILE_LOCATION
flat_src = Config.FLAT_FILE_SOURCE
coll_src = Config.COLLECTIONS_FILE_SOURCE


file_to_upload = "Jonah.Hex (2010).mp4"
f_list = get_movie_file_path_list(file_to_upload)
title = ''
year = ''
for f in f_list:
    title = f['title']
    year = f['year']
imdb_id = get_movie_id(title, int(year), 1)

print(type(imdb_id))
print(imdb_id)


# for f in file_list:
#     yield f
#     print(f)
# app = create_app()
# with app.app_context():
#     created = create_movie(file_list[0], app)
# print(created)


# files = get_files(Config.FLAT_FILE_SOURCE)
# for file in files:
#     print(file)


# app = create_app()
# with app.app_context():
#     scrape_imdb()


# sub_dirs = list(folders_in(debug_path))
# if not sub_dirs:
#     print(f'List for {sub_dirs} is empty')
# else:
#     for dir in sub_dirs:
#         print(dir)
# title = '300.Rise.of.an.Empire'.replace('.', ' ').rsplit()
# imdb_id = get_movie_id(title, 2014, 1)
# movie = get_movie(imdb_id)
# print(imdb_id)
# print(movie['title'])
# print(movie['kind'])
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
    files = get_files(source)
    ctr = 0
    for file in files:
        ctr += 1
        _id = get_movie_id(str(file['title']), int(file['year']), ctr)
        film = get_movie(_id)
        if file['title'].lower() != film['title'].lower().replace(':', '').replace('.', ' '). \
                replace('...', '   ').rstrip():
            print(f'******WARNING**** Movie is potentially missing {file["title"]}')
