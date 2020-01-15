# author        :   ignorantshr
# create_date   :   2020/01/15 3:43 PM
# description   :   authentication Blueprint

import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

# define a blueprint with name 'auth'
bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        error_msg = None
        username = request.form.get('username', None)
        password = request.form.get('password', None)
        db = get_db()

        if not username or not password:
            error_msg = 'username and password is required.'
        elif db.execute('SELECT id FROM user WHERE username = ?', (username,))\
               .fetchone() is not None:
            error_msg = 'user {} has already registered'.format(username)

        if error_msg is None:
            db.execute('INSERT INTO user (username, password) VALUES (?, ?)',
                       (username, generate_password_hash(password)))
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error_msg)

    return render_template('auth/register.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        error_msg = None
        username = request.form.get('username', None)
        password = request.form.get('password', None)
        db = get_db()

        if not username or not password:
            error_msg = 'username and password is required.'
            flash(error_msg)
            return redirect(url_for('auth.login'))

        user = db.execute('SELECT * FROM user WHERE username = ?', (username,))\
                 .fetchone()

        if user is None:
            error_msg = 'Incorrect username'
        elif not check_password_hash(user['password'], password):
            error_msg = 'Incorrect password'

        if error_msg is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error_msg)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute('SELECT * FROM user WHERE id = ?',
                                  (user_id,)).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


def login_required(view):
    @functools.wraps(view)
    def wrapper(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapper
