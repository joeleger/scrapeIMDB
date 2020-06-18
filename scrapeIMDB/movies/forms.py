from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FloatField, TextAreaField
from wtforms.validators import DataRequired, Length


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
    box_office = FloatField('Box Office', validators=[DataRequired()])
    submit = SubmitField('Save')
