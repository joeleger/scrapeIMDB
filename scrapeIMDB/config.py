from os import environ


class Config:
    FLAT_FILE_SOURCE = 'F:\\Video\Movies\\_Flat_Structure'
    COLLECTIONS_FILE_SOURCE = 'F:\\Video\\Movies\\_Collections'
    SECRET_KEY = environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///movieListing.db'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = environ.get('EMAIL_USER')
    MAIL_PASSWORD = environ.get('EMAIL_PASS')