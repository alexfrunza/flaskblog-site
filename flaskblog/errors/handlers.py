from flask import Blueprint, render_template, redirect, url_for
from flaskblog.posts.forms import SearchForm

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
def error_404(error):
    search_form = SearchForm()
    if search_form.validate_on_submit():
        return redirect(url_for('main.search', results_for=search_form.search_field.data))

    return render_template('errors/404.html', search_form=search_form), 404


@errors.app_errorhandler(403)
def error_403(error):
    search_form = SearchForm()
    if search_form.validate_on_submit():
        return redirect(url_for('main.search', results_for=search_form.search_field.data))

    return render_template('errors/403.html', search_form=search_form), 403


@errors.app_errorhandler(500)
def error_500(error):
    search_form = SearchForm()
    if search_form.validate_on_submit():
        return redirect(url_for('main.search', results_for=search_form.search_field.data))

    return render_template('errors/500.html', search_form=search_form), 500