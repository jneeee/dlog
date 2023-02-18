from os import getenv

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
            flash(f"Login success {form.get('username')}", 'message')
        else:
            flash(f"Login failed {form.get('username')}", 'warning')
        return redirect(url_for('index'))

@bp_user.route("/register", methods=["GET", 'POST'])
def register():
    if request.method == 'GET':
        return render_template('user/register.html')
    elif request.method == 'POST':
        if getenv('ALLOW_REGISTER') != 'True':
            flash('Register is not allowed now.', 'warning')
            return render_template('user/register.html')
        try:
            User.create_user(request.form)
        except ValueError as e:
            flash(f'Error: {e}', 'error')
        else:
            flash(f'User {request.form} register success', 'message')
        return redirect(url_for('user.login'))

@bp_user.route("/logout", methods=["GET"])
def logout():
    nm = session.pop('username')
    flash(f"Logout success: {nm}", 'message')
    return redirect(url_for('user.login'))
