from flask import Blueprint, request, render_template, flash

from detautils.utils import login_required
from bluep.object.post import Post

bp_post = Blueprint('post', __name__, url_prefix="/post")

@bp_post.route("/new", methods=["GET", 'POST'])
@login_required
def post():
    if request.method =='GET':
        return render_template('post.html')
    elif request.method == 'POST':
        flash(f'form: {request.form}')
        return render_template('post.html')

@bp_post.route("/<post_id>", methods=["GET"])
def post_detail(post_id):
    try:
        Post.get_post_info_by_key(post_id)
    except ValueError:
        