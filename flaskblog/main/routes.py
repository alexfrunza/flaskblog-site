from flask import Blueprint, render_template, request, redirect, url_for
from flaskblog.models import Post
from sqlalchemy import or_
from flaskblog.posts.forms import SearchForm

main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
@main.route('/home', methods=['GET', 'POST'])
def home():
    search_form = SearchForm()
    if search_form.validate_on_submit():
        return redirect(url_for('main.search', results_for=search_form.search_field.data))

    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts, search_form=search_form)


@main.route('/about', methods=['GET', 'POST'])
def about():
    search_form = SearchForm()
    if search_form.validate_on_submit():
        return redirect(url_for('main.search', results_for=search_form.search_field.data))

    return render_template('about.html', title='About', search_form=search_form)


@main.route('/search', methods=['GET', 'POST'])
def search():
    search_form = SearchForm()
    if search_form.validate_on_submit():
        return redirect(url_for('main.search', results_for=search_form.search_field.data))

    page = request.args.get('page', 1, type=int)
    search_str = request.args.get('results_for', type=str)
    search_results = Post.query.filter(or_(
        Post.title.ilike(f'%{search_str}%'),
        Post.content.ilike(f'%{search_str}%')
    )).paginate(page=page, per_page=5)
    return render_template('search.html', posts=search_results, search_form=search_form,
                           location='search', search_str=search_str)
