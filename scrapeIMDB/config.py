from os import environ


class Config:
    # File Source configuration locations
    FLAT_FILE_SOURCE = 'F:\\Video\\\Movies\\_Flat_Structure'
    COLLECTIONS_FILE_SOURCE = 'F:\\Video\\Movies\\_Collections'
    DEBUG_FILE_LOCATION = 'F:\\Video\\Movies\\Debug'

    SECRET_KEY = environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///movieListing.db'

    # Mail configuration
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = environ.get('EMAIL_USER')
    MAIL_PASSWORD = environ.get('EMAIL_PASS')

    # Elasticsearch properties
    ELASTICSEARCH_URL = environ.get('ELASTICSEARCH_URL')
    MOVES_PER_PAGE = 5
