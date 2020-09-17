from flask import (Blueprint, render_template, url_for, flash,
                   redirect, request, abort)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Post, PostComment
from flaskblog.posts.forms import PostForm, PostCommentForm, SearchForm

posts = Blueprint('posts', __name__)


@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    search_form = SearchForm()
    if search_form.validate_on_submit():
        return redirect(url_for('main.search', results_for=search_form.search_field.data))

    form = PostForm()
    if form.validate_on_submit():
        user_post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(user_post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post', form=form, search_form=search_form)


@posts.route('/post/<int:post_id>', methods=['GET', "POST"])
def post(post_id):
    search_form = SearchForm()
    if search_form.validate_on_submit():
        return redirect(url_for('main.search', results_for=search_form.search_field.data))

    user_post = Post.query.get_or_404(post_id)
    comments = user_post.comments.order_by(PostComment.date_posted.desc())
    form = PostCommentForm()
    if form.validate_on_submit() and current_user.is_authenticated:
        user_comment = PostComment(user=current_user, post=user_post, content=form.content.data)
        db.session.add(user_comment)
        db.session.commit()
        flash('Your comment has been posted!', 'success')
        return redirect(request.path)
    return render_template('post.html', title=user_post.title, post=user_post, form=form, comments=comments,
                           search_form=search_form)


@posts.route('/post/<int:post_id>/update', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    search_form = SearchForm()
    if search_form.validate_on_submit():
        return redirect(url_for('main.search', results_for=search_form.search_field.data))

    user_post = Post.query.get_or_404(post_id)
    if user_post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        user_post.title = form.title.data
        user_post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=user_post.id))
    elif request.method == 'GET':
        form.title.data = user_post.title
        form.content.data = user_post.content
    return render_template('create_post.html', title='Update Post', form=form, search_form=search_form)


@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    user_post = Post.query.get_or_404(post_id)
    if user_post.author != current_user:
        abort(403)
    db.session.delete(user_post)
    db.session.commit()
    flash("Your post has been deleted!", 'success')
    return redirect(url_for('main.home'))


@posts.route('/like/<int:post_id>/like')
@login_required
def like_action(post_id):
    user_post = Post.query.get_or_404(post_id)
    current_user.like_post(user_post)
    db.session.commit()
    return redirect(request.referrer)


@posts.route('/like/<int:post_id>/dislike')
@login_required
def dislike_action(post_id):
    user_post = Post.query.get_or_404(post_id)
    current_user.dislike_post(user_post)
    db.session.commit()
    return redirect(request.referrer)


@posts.route('/post/<int:post_id>/comment/<int:comment_id>/update', methods=['GET', 'POST'])
@login_required
def update_comment(post_id, comment_id):
    search_form = SearchForm()
    if search_form.validate_on_submit():
        return redirect(url_for('main.search', results_for=search_form.search_field.data))

    user_post = Post.query.get_or_404(post_id)
    user_comment = PostComment.query.get_or_404(comment_id)
    if user_comment.user != current_user:
        abort(403)
    form = PostCommentForm()
    if form.validate_on_submit():
        user_comment.content = form.content.data
        db.session.commit()
        flash('Your comment has been updated!', 'success')
        return redirect(url_for('posts.post', post_id=user_post.id))
    elif request.method == 'GET':
        form.content.data = user_comment.content
    return render_template('update_comment.html', form=form, title='Update Comment', search_form=search_form)


@posts.route('/post/<int:post_id>/comment/<int:comment_id>/delete')
@login_required
def delete_comment(post_id, comment_id):
    user_post = Post.query.get_or_404(post_id)
    user_comment = PostComment.query.get_or_404(comment_id)
    if user_comment.user == current_user or user_post.author == current_user:
        db.session.delete(user_comment)
        db.session.commit()
        flash("You deleted a comment!", 'success')
        return redirect(request.referrer)
    abort(403)