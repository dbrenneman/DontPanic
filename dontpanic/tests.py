import unittest

from .models import DBSession


class TestMyView(unittest.TestCase):
    def setUp(self):
        self.config = testing.setUp()
        from sqlalchemy import create_engine
        engine = create_engine('sqlite://')
        from .models import (
            Base,
            Article,
            )
        DBSession.configure(bind=engine)
        Base.metadata.create_all(engine)
        with transaction.manager:
            model = Article(title='one', body='foo')
            DBSession.add(model)

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

    def test_blog_view(self):
        from .views import blog_view
        request = testing.DummyRequest()
        info = blog_view(request)
        self.assertEqual(info['page_title'], 'Blog')
        self.assertEqual(info['one'].title, 'one')

    def test_home_view(self):
        from .views import home_view
        request = testing.DummyRequest()
        info = home_view(request)
        self.assertEqual(info['page_title'], 'Home')
