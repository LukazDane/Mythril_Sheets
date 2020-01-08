from flask import Flask, render_template, request, redirect, url_for, flash
import os
from config import Config
from forms import LoginForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import models

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('home'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/')
def home():
    """Display home page"""
    return render_template("home.html")

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)


@app.route('/library')
def library():
    """Display's all dnd info, according to homebrew, like a wiki"""
    return render_template("library.html")


@app.route('/sheets')
def sheets():
    """Displays Character sheets"""
    return render_template("sheets.html")


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
