from flask import Flask, render_template

from bluep.user import user
from bluep.post import post


app = Flask(__name__)
app.secret_key = '495e4486ef931ad5c8a66126ea13d31cac98526fad5a59620e7b314662ac7434'

app.register_blueprint(user.bp_user)
app.register_blueprint(post.bp_post)


@app.route('/', methods=["GET"])
def index():
    return render_template('index.html')
