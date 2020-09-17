from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, discord_oauth
from passlib.hash import argon2
from flaskblog.models import User, Post
from flaskblog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   ResetPasswordForm, RequestResetForm)
from flaskblog.users.utils import save_picture, send_reset_email
from flaskblog.posts.forms import SearchForm

users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()

    search_form = SearchForm()
    if search_form.validate_on_submit():
        return redirect(url_for('main.search', results_for=search_form.search_field.data))

    if form.validate_on_submit():
        hashed_password = argon2.hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You are able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Register', form=form, search_form=search_form)


@users.route('/login', methods=['GET', "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()

    search_form = SearchForm()
    if search_form.validate_on_submit():
        return redirect(url_for('main.search', results_for=search_form.search_field.data))

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and argon2.verify(form.password.data, user.password):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash("Login unsuccessful. Please check email and password", 'danger')
    return render_template('login.html', title='Login', form=form, search_form=search_form)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    search_form = SearchForm()
    if search_form.validate_on_submit():
        return redirect(url_for('main.search', results_for=search_form.search_field.data))

    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static',
                         filename=f'profile_pics/{current_user.image_file}')
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form, search_form=search_form)


@users.route('/user/<string:username>', methods=['GET', "POST"])
def user_posts(username):
    search_form = SearchForm()
    if search_form.validate_on_submit():
        return redirect(url_for('main.search', results_for=search_form.search_field.data))

    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user, search_form=search_form)


@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():

    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()

    search_form = SearchForm()
    if search_form.validate_on_submit():
        return redirect(url_for('main.search', results_for=search_form.search_field.data))

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to set your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form, search_form=search_form)


@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if not user:
        flash('That is an invalid or expired token!', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()

    search_form = SearchForm()
    if search_form.validate_on_submit():
        return redirect(url_for('main.search', results_for=search_form.search_field.data))

    if form.validate_on_submit():
        hashed_password = argon2.hash(form.password.data)
        user.password = hashed_password
        db.session.commit()
        flash(f'Your password had been updated! You are able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form, search_form=search_form)


@users.route('/login_with_discord')
def login_with_discord():
    return discord_oauth.create_session(scope=['identify', 'email'])


@users.route('/oauth_discord')
def callback():
    discord_oauth.callback()
    discord_user = discord_oauth.fetch_user()
    user = User.query.filter_by(discord_id=int(discord_user.id)).first()

    if current_user.is_authenticated and user:
        return redirect('main.home')
    if current_user.is_authenticated and not user:
        current_user.discord_id = discord_user.id
        db.session.commit()
        discord_oauth.revoke()
        return redirect(url_for('main.home'))

    if not user and User.query.filter_by(email=discord_user.email).first():
        flash('If you have already an account you must connect your account with discord, before log in with discord!', 'warning')
        return redirect(url_for('users.login'))

    if not user:
        user = User(username=discord_user.username, email=discord_user.email, discord_id=discord_user.id)
        db.session.add(user)
        db.session.commit()

    login_user(user)
    discord_oauth.revoke()
    return redirect(url_for('main.home'))


