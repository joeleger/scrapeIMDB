from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, FloatField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from scrapeIMDB.models import User


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


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
