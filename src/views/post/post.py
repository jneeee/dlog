from flask import Blueprint, request, render_template, flash, \
    abort, session

from utils import login_required
from views.object.post import Post

bp_post = Blueprint('post', __name__, url_prefix="/post")

@bp_post.route("/new", methods=["GET", 'POST'])
@login_required
def post():
    if request.method =='GET':
        return render_template('post.html')
    elif request.method == 'POST':
        ins = Post(request.form,
                   author_name=session.get('username'))
        ins.save()
        flash(f'Create post success: {ins.key}')
        return render_template('post.html')

@bp_post.route("/<post_id>", methods=["GET"])
def post_detail(post_id):
    try:
        Post.get_post_info_by_key(post_id)
    except ValueError:
        abort(404)
