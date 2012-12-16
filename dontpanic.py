# -*- coding: utf-8 -*-
"""
    DontPanic
    ~~~~~~

    A blog based on Armin Ronacher's Flaskr example app.

    :copyright: (c) 2012 by David Brenneman
    :license: BSD, see LICENSE for more details.
"""
from __future__ import with_statement
import datetime
import os
from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash, _app_ctx_stack

# configuration
YEAR = datetime.datetime.now().year
HERE = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.path.join(HERE, 'dontpanic.db')
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('DONTPANIC_SETTINGS', silent=True)


def init_db():
    """Creates the database tables."""
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    top = _app_ctx_stack.top
    if not hasattr(top, 'sqlite_db'):
        top.sqlite_db = sqlite3.connect(app.config['DATABASE'])
    return top.sqlite_db


@app.teardown_appcontext
def close_db_connection(exception):
    """Closes the database again at the end of the request."""
    top = _app_ctx_stack.top
    if hasattr(top, 'sqlite_db'):
        top.sqlite_db.close()


@app.route('/')
def show_homepage():
    return render_template('home.html', year=YEAR)


@app.route('/blog')
def show_entries():
    db = get_db()
    cur = db.execute('select title, text from entries order by id desc')
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('blog.html', entries=entries, year=YEAR)


@app.route('/blog/<slug>')
def show_entry():
    db = get_db()
    cur = db.execute('select slug, title, text from entries order by id desc where slug=%s' % slug)
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('blog.html', entries=entries, year=YEAR)


@app.route('/blog/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    db.execute('insert into entries (title, text) values (?, ?)',
               [request.form['title'], request.form['text']])
    db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


if __name__ == '__main__':
    init_db()
    app.run()
