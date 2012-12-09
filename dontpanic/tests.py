import unittest
import transaction

from pyramid import testing

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

    def test_about_view(self):
        from .views import about_view
        request = testing.DummyRequest()
        info = about_view(request)
        self.assertEqual(info['page_title'], 'About')

    def test_blog_view(self):
        from .views import blog_view
        request = testing.DummyRequest()
        info = blog_view(request)
        self.assertEqual(info['page_title'], 'Blog')
        self.assertEqual(info['one'].title, 'one')

    def test_contact_view(self):
        from .views import contact_view
        request = testing.DummyRequest()
        info = contact_view(request)
        self.assertEqual(info['page_title'], 'Contact')

    def test_home_view(self):
        from .views import home_view
        request = testing.DummyRequest()
        info = home_view(request)
        self.assertEqual(info['page_title'], 'Home')
