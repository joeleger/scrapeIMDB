from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from os import environ

app = Flask(__name__)
app.config['SECRET_KEY'] = environ.get("SECRET_KEY")

movies = [
    {
        'title': 'Cleopatra',
        'year': '1963',
        'plot': 'This is the plot of the movie.',
        'cast': 'Elizabeth Taylor, Richard Burton, Rex Harrison',
        'date_posted': 'June 12, 2020'
    },
    {
        'title': 'Avengers: Endgame',
        'year': '2019',
        'plot': 'This is the plot of the movie.',
        'cast': 'Robert Downey Jr., Chris Evans, Mark Ruffalo',
        'date_posted': 'June 12, 2020'
    }
]


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', movies=movies)


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/register', methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))

    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash(f'You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash(f'Login was unsuccessful! Please check username and password.', 'danger')
    return render_template('login.html', title='Login', form=form)


if __name__ == "__main__":
    app.run(debug=True)
