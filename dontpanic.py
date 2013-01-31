# -*- coding: utf-8 -*-
"""
    DontPanic
    ~~~~~~

    A blog based on Armin Ronacher's Flaskr example app.

    :copyright: (c) 2013 by David Brenneman
    :license: BSD, see LICENSE for more details.
"""
from __future__ import with_statement
import datetime
from htmlmin.minify import html_minify
import markdown
import os
import sqlite3
from urlparse import urljoin
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash, _app_ctx_stack
from werkzeug.contrib.atom import AtomFeed

# configuration
YEAR = datetime.datetime.now().year
HERE = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.path.join(HERE, '..', 'dontpanic.db')
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('DONTPANIC_SETTINGS', silent=True)


def make_external(url):
    return urljoin(request.url_root, url)


def init_db():
    """Creates the database tables."""
    with app.app_context():
        db = connect_db()
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()


def connect_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    top = _app_ctx_stack.top
    if not hasattr(top, 'sqlite_db'):
        top.sqlite_db = sqlite3.dbapi2.connect(
            app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,)
    return top.sqlite_db


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_appcontext
def close_db_connection(exception):
    """Closes the database again at the end of the request."""
    top = _app_ctx_stack.top
    if hasattr(top, 'sqlite_db'):
        top.sqlite_db.close()


@app.route('/')
def show_homepage():
    return html_minify(render_template('home.html', year=YEAR))


@app.route('/blog')
def show_articles():
    cur = g.db.execute(
        'select title, slug, published from articles order by published')
    articles = [
        dict(title=row[0],
             slug=row[1],
             published=row[2].strftime('%d %B, %Y')) for row in cur.fetchall()]
    return html_minify(
        render_template(
            'blog.html', articles=articles, page_title='Blog | ', year=YEAR))


@app.route('/blog/recent.atom')
def recent_feed():
    feed = AtomFeed('David Brenneman',
                    feed_url=request.url, url=request.url_root)
    cur = g.db.execute(
        'select title, slug, body, updated as "updated [timestamp]",'
        ' published as "published [timestamp]" from articles order by updated')
    articles = [dict(title=row[0],
                     slug=row[1],
                     body=row[2],
                     updated=row[3],
                     published=row[4]) for row in cur.fetchall()]
    for article in articles:
        body = markdown.markdown(article['body'])
        feed.add(
            article['title'],
            body,
            content_type='html',
            author='David Brenneman',
            url=make_external(url_for('show_article', slug=article['slug'])),
            updated=article['updated'],
            published=article['published'])
    return feed.get_response()


@app.route('/blog/add', methods=['GET', 'POST'])
def add_article():
    if not session.get('logged_in'):
        abort(401)
    if request.method == 'POST':
        now = datetime.datetime.now()
        g.db.execute(('insert into articles (title, slug, body, updated, '
                      'published) values (?, ?, ?, ?, ?)'),
                     [request.form['title'],
                      request.form['slug'],
                      request.form['body'],
                      now,
                      now
                      ])
        g.db.commit()
        flash('New article was successfully posted')
        return redirect(url_for('show_articles'))
    else:
        title = "Add Article | "
        return html_minify(render_template('blog_add.html',
                                           page_title=title,
                                           year=YEAR))


@app.route('/blog/<slug>')
def show_article(slug):
    cur = g.db.execute(('select title, body, slug, published from articles '
                        'where slug=? order by published desc'), [slug])
    article = None
    articles = [
        dict(title=row[0],
             body=row[1],
             slug=row[2],
             published=row[3].strftime('%d %B, %Y')) for row in cur.fetchall()]
    if articles:
        article = articles[0]
        article['body'] = markdown.markdown(
            article['body'], output_format="html5")
        page_title = article['title']  + ' | '
        return html_minify(render_template('blog_page.html',
                                           article=article,
                                           page_title=page_title,
                                           year=YEAR))
    else:
        abort(404)


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
            return redirect(url_for('add_article'))
    return html_minify(render_template('login.html', error=error))


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_articles'))


@app.errorhandler(404)
def page_not_found(e):
    return html_minify(render_template('404.html'), 404)


@app.errorhandler(500)
def application_error(e):
    return html_minify(render_template('500.html'), 500)

if __name__ == '__main__':
    init_db()
    app.run()
