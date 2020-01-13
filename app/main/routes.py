from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app
from flask_login import current_user, login_required
from flask_babel import _, get_locale
from app import db
from app.main.forms import EditProfileForm, SheetForm
from app.models import User, Sheet
from app.main import bp


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/home', methods=['GET', 'POST'])
def home():
    """Display home page"""
    return render_template("home.html")


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    sheets = user.sheets.order_by(Sheet.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('main.user', username=user.username, page=sheets.next_num) \
        if sheets.has_next else None
    prev_url = url_for('main.user', username=user.username, page=sheets.prev_num) \
        if sheets.has_prev else None
    return render_template('user.html', user=user, sheets=sheets.items,
                           next_url=next_url, prev_url=prev_url)


@bp.route('/library')
def library():
    """Display's all dnd info, according to homebrew, like a wiki"""
    return render_template("library.html")


@bp.route('/pages', methods=['GET', 'POST'])
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
        return redirect(url_for('main.pages'))
    sheets = current_user.followed_sheets().all()
    return render_template("sheets.html", title='Sheets', sheets=sheets, form=form)
    page = request.args.get('page', 1, type=int)
    sheets = current_user.followed_sheets().paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('sheets', page=sheets.next_num) \
        if sheets.has_next else None
    prev_url = url_for('sheets', page=sheets.prev_num) \
        if sheets.has_prev else None
    return render_template('sheets.html', title='Sheets', form=form,
                           sheets=sheets.items, next_url=next_url,
                           prev_url=prev_url)


@bp.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.user', username=current_user.username))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


@bp.route('/delete', methods=['GET', 'POST', 'DELETE'])
@login_required
def delete(id):
    sheet = Sheet.query.get(id, **req_args)
    if sheet is None:
        flash('Charactr not found!')
        return redirect(url_for('main.sheets',))
    if sheet.author.id != g.user.id:
        flash('You cannot delete this Character.')
        return redirect(url_for('main.sheets'))
    g.db.execute(id)
    flash('Your post has been deleted.')
    return redirect(url_for('main.sheets'))


@bp.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('main.home'))
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('main.user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}!'.format(username))
    return redirect(url_for('main.user', username=username))


@bp.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('main.home'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('main.user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}.'.format(username))
    return redirect(url_for('main.user', username=username))


@bp.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    sheets = Sheet.query.order_by(Sheet.timestamp.desc()).paginate(
        page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('explore', page=sheets.next_num) \
        if sheets.has_next else None
    prev_url = url_for('explore', page=sheets.prev_num) \
        if sheets.has_prev else None
    return render_template('sheets.html', title='Explore', sheets=sheets.items, next_url=next_url, prev_url=prev_url)
