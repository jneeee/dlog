from os import getenv

from flask import Flask, render_template

from views.user import user
from views.post import post
from views.object.post import Post

app = Flask(__name__)
app.secret_key = getenv('DETA_PROJECT_KEY')

app.register_blueprint(user.bp_user)
app.register_blueprint(post.bp_post)


@app.route('/', methods=["GET"])
def index():
    # res: {count:num, last:xx, items:[{}, ]}
    res = Post.fetch_posts()
    return render_template('index.html', items=res.items)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404
