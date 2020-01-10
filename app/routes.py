from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, SheetForm, ResetPasswordRequestForm, ResetPasswordForm, EditSheetForm
from app.email import send_password_reset_email
from flask_login import current_user, login_user, login_required, logout_user
from app.models import User, Sheet
from werkzeug.urls import url_parse
from datetime import datetime


#############################################
# Login
#############################################
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
        # return redirect(url_for('home'))
    return render_template('login.html', title='Sign In', form=form)

#############################################
# Log0ut
#############################################
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

#############################################
# Register
#############################################
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

#############################################
# Password Reset Request
#############################################
@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)

#############################################
# Password Reset Route
#############################################
@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('home'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)


@app.route('/')
@app.route('/home')
def home():
    """Display home page"""
    return render_template("home.html")


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    sheets = user.sheets.order_by(Sheet.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('user', username=user.username, page=sheets.next_num) \
        if sheets.has_next else None
    prev_url = url_for('user', username=user.username, page=sheets.prev_num) \
        if sheets.has_prev else None
    return render_template('user.html', user=user, sheets=sheets.items,
                           next_url=next_url, prev_url=prev_url)


@app.route('/library')
def library():
    """Display's all dnd info, according to homebrew, like a wiki"""
    return render_template("library.html")


@app.route('/pages', methods=['GET', 'POST'])
@login_required
def pages():
    """Displays Character sheets"""
    form = SheetForm()
    if form.validate_on_submit():
        sheet = Sheet(
            body=form.body.data, author=current_user, character_name=form.character_name.data, level=form.level.data, race=form.race.data, job=form.job.data)
        db.session.add(sheet)
        db.session.commit()
        flash('Your Character lives!')
        return redirect(url_for('pages'))
    sheets = current_user.followed_sheets().all()
    return render_template("sheets.html", title='Sheets', sheets=sheets, form=form)
    page = request.args.get('page', 1, type=int)
    sheets = current_user.followed_sheets().paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('sheets', page=sheets.next_num) \
        if sheets.has_next else None
    prev_url = url_for('sheets', page=sheets.prev_num) \
        if sheets.has_prev else None
    return render_template('sheets.html', title='Sheets', form=form,
                           sheets=sheets.items, next_url=next_url,
                           prev_url=prev_url)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)

# @app.route('/edit_sheet', methods=['GET', 'POST'])
# @login_required
# def edit_sheet():
#     form = EditSheetForm()


@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('home'))
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}!'.format(username))
    return redirect(url_for('user', username=username))


@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('home'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}.'.format(username))
    return redirect(url_for('user', username=username))


@app.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    sheets = Sheet.query.order_by(Sheet.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('explore', page=sheets.next_num) \
        if sheets.has_next else None
    prev_url = url_for('explore', page=sheets.prev_num) \
        if sheets.has_prev else None
    return render_template('sheets.html', title='Explore', sheets=sheets.items, next_url=next_url, prev_url=prev_url)
