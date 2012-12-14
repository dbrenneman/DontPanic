import datetime


from sqlalchemy.exc import DBAPIError

from .models import (
    DBSession,
    Article,
    )

YEAR = datetime.datetime.now().year


@view_config(route_name='blog', renderer='blog.jinja2')
def blog_view(request):
    try:
        articles = DBSession.query(Article).all()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'page_title': 'Blog',
            'one': one,
            'year': YEAR,
           }


@view_config(route_name='blog_page', renderer='blog_page.jinja2')
def blog_page_view(request):
    try:
        articles = DBSession.query(Article).all()
    except DBAPIError:
        return Response(conn_err_msg, content_type='text/plain', status_int=500)
    return {'page_title': 'Blog',
            'one': one,
            'year': YEAR,
           }


@view_config(route_name='home', renderer='home.jinja2')
def home_view(request):
    return {'page_title': 'Home',
            'year': YEAR,
           }
