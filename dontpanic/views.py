import datetime
from . import app

from flask import render_template

YEAR = datetime.datetime.now().year


@app.route('/')
def home_view(request):
    return render_template('home.jinja2',
                           title='Home',
                           year=YEAR,
    )


@app.route('/blog')
def blog_view(request):
    return render_template('blog.jinja2',
                           title='Blog',
                           year=YEAR,
    )


@app.route('/blog/<slug>')
def blog_page_view(request):
    return render_template('blog_page.jinja2',
                           title='Blog',
                           year=YEAR,
    )
