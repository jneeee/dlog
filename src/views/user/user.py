from flask import Blueprint, request, flash, redirect, url_for, \
    render_template, session

from views.object.user import User


bp_user = Blueprint('user', __name__, url_prefix="/user")

@bp_user.route("/login", methods=["GET", 'POST'])
def login():
    if request.method == 'GET':
        return render_template('user/login.html')
    elif request.method == 'POST':
        form = request.form
        if User.check_login_valid(form):
            session['username'] = form.get('username')
            flash(f"登录成功 {form.get('username')}")
        else:
            flash(f"登录失败 {form.get('username')}")
        return redirect(url_for('index'))

@bp_user.route("/register", methods=["GET", 'POST'])
def register():
    if request.method == 'GET':
        return render_template('user/register.html')
    elif request.method == 'POST':
        try:
            User.create_user(request.form)
        except ValueError as e:
            flash(f'Error: {e}')
        else:
            flash(f'用户 {request.form} 注册成功')
        return redirect(url_for('user.login'))

@bp_user.route("/logout", methods=["GET"])
def logout():
    nm = session.pop('username')
    flash(f"登出成功 {nm}")
    return redirect(url_for('user.login'))
