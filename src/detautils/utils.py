import functools
from threading import Thread

from flask import g, redirect, url_for, session
from deta import Deta


deta = Deta()
db = deta.Base('dreamlog')

def async_exc(func):
    def wrap(*args, **kwargs):
        Thread(func, *args, **kwargs).start()

    return wrap

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if 'username' not in session:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
