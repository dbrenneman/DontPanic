import datetime
from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    Article,
    )

YEAR = datetime.datetime.now().year


@view_config(route_name='about', renderer='about.jinja2')
def about_view(request):
    return {'page_title': 'About',
            'year': YEAR,
           }


@view_config(route_name='blog', renderer='blog.jinja2')
def blog_view(request):
    try:
        one = DBSession.query(Article).filter(Article.title=='one').first()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'page_title': 'Blog',
            'one': one,
            'project': 'DontPanic',
            'year': YEAR,
           }


@view_config(route_name='contact', renderer='contact.jinja2')
def contact_view(request):
    return {'page_title': 'Contact',
            'year': YEAR,
           }


@view_config(route_name='home', renderer='home.jinja2')
def home_view(request):
    return {'page_title': 'Home',
            'year': YEAR,
           }


conn_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_DontPanic_db" script
    to initialize your database tables.  Check your virtual 
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""
