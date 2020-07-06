from flask import request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FloatField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError
from scrapeIMDB.models import Movie


class NewMovieForm(FlaskForm):
    imdb_id = StringField('IMDB_ID', validators=[DataRequired(), Length(min=5, max=50)])
    file_path = StringField('File Path', validators=[DataRequired(), Length(max=300)])
    title = StringField('Title', validators=[DataRequired(), Length(max=500)])
    year = IntegerField('Year', validators=[DataRequired()])
    genre = StringField('Genre', validators=[DataRequired(), Length(max=100)])
    rating = FloatField('Rating', validators=[DataRequired()])
    actors = StringField('Cast', validators=[DataRequired(), Length(max=5000)])
    directors = StringField('Directors', validators=[DataRequired(), Length(max=300)])
    writers = StringField('Writers', validators=[DataRequired(), Length(max=300)])
    plot = TextAreaField('Plot', validators=[DataRequired()])
    runtime = IntegerField('Runtime', validators=[DataRequired()])
    poster_url = StringField('Poster Url', validators=[DataRequired(), Length(max=500)])
    submit = SubmitField('Save')

    def validate_imdb_id(self, imdb_id):
        film = Movie.query.filter_by(imdb_id=imdb_id.data).first()
        if film:
            raise ValidationError('That imdb_id already exists. You can only add the movie once!')


class UpdateMovieForm(FlaskForm):
    # imdb_id = StringField('IMDB_ID', render_kw={'readonly': True})
    file_path = StringField('File Path', validators=[DataRequired(), Length(max=300)])
    title = StringField('Title', validators=[DataRequired(), Length(max=500)])
    year = IntegerField('Year', validators=[DataRequired()])
    genre = StringField('Genre', validators=[DataRequired(), Length(max=100)])
    rating = FloatField('Rating', validators=[DataRequired()])
    actors = StringField('Cast', validators=[DataRequired(), Length(max=5000)])
    directors = StringField('Directors', validators=[DataRequired(), Length(max=300)])
    writers = StringField('Writers', validators=[DataRequired(), Length(max=300)])
    plot = TextAreaField('Plot', validators=[DataRequired()])
    runtime = IntegerField('Runtime', validators=[DataRequired()])
    poster_url = StringField('Poster Url', validators=[DataRequired(), Length(max=500)])
    submit = SubmitField('Save')


class SearchForm(FlaskForm):
    q = StringField('Search', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)
