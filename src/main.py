from os import getenv

from flask import Flask, render_template, g, redirect, url_for, request, flash

from views.user import user
from views.post import post
from views.object.post import Post
from utils import db

app = Flask(__name__)
app.secret_key = getenv('DETA_PROJECT_KEY')
app.config['site_info'] = db.get('site_info')

app.register_blueprint(user.bp_user)
app.register_blueprint(post.bp_post)


@app.route('/', methods=["GET"])
def index():
    if not app.config['site_info']:
        return redirect(url_for('setup'))

    items = Post.fetch_posts()
    return render_template('index.html', items=items)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


@app.route('/tags/<tag>', methods=["GET"])
def tags(tag):
    items = Post.fetch_by_tag(tag)
    return render_template('index.html', items=items)


@app.route('/setup', methods=["GET", "POST"])
def setup():
    if request.method == 'GET':
        if not app.config['site_info']:
            return render_template('setup.html')
        else:
            flash('Site info has been completed! You can change change them in deta base or install a new app', 'warning')
            return redirect(url_for('index'))
    elif request.method == 'POST':
        form = request.form
        item = {
            'site_title': form.get('site_title'),
            'description': form.get('description'),
            'brand': form.get('brand'),
        }
        db.put(item, 'site_info')
        app.config['site_info'] = item
        flash('Site info complite!', 'message')
        return redirect(url_for('index'))
