# -*- coding: utf-8 -*-
"""
    DontPanic Tests
    ~~~~~~~~~~~~

    Tests for the DontPanic application.

    :copyright: (c) 2013 by David James Brenneman.
    :license: BSD, see LICENSE for more details.
"""
import os
import dontpanic
import unittest
import tempfile


class DontPanicTestCase(unittest.TestCase):

    def setUp(self):
        """Before each test, set up a blank database"""
        self.db_fd, dontpanic.app.config['DATABASE'] = tempfile.mkstemp()
        dontpanic.app.config['TESTING'] = True
        self.app = dontpanic.app.test_client()
        dontpanic.init_db()

    def tearDown(self):
        """Get rid of the database again after each test."""
        os.close(self.db_fd)
        os.unlink(dontpanic.app.config['DATABASE'])

    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    # testing functions

    def test_empty_db(self):
        """Start with a blank database."""
        rv = self.app.get('/blog')
        assert 'Unbelievable' in rv.data

    def test_login_logout(self):
        """Make sure login and logout works."""
        rv = self.login(dontpanic.app.config['USERNAME'],
                        dontpanic.app.config['PASSWORD'])
        assert '<form action="/blog/add" method=post class=add-article>' in rv.data
        rv = self.logout()
        assert '<form action="/blog/add" method=post class=add-article>' not in rv.data
        rv = self.login(dontpanic.app.config['USERNAME'] + 'x',
                        dontpanic.app.config['PASSWORD'])
        assert 'Invalid username' in rv.data
        rv = self.login(dontpanic.app.config['USERNAME'],
                        dontpanic.app.config['PASSWORD'] + 'x')
        assert 'Invalid password' in rv.data

    def test_articles(self):
        """Test that posting articles works."""
        self.login(dontpanic.app.config['USERNAME'],
                   dontpanic.app.config['PASSWORD'])
        slug = 'hello'
        rv = self.app.post('/blog/add', data=dict(
            title='<Hello>',
            slug=slug,
            body='<strong>HTML</strong> allowed here'
        ), follow_redirects=True)
        assert 'Unbelievable' not in rv.data
        assert '&lt;Hello&gt;' in rv.data
        assert 'New article was successfully posted' in rv.data
        rv = self.app.get('/blog/' + slug)
        assert '<strong>HTML</strong> allowed here' in rv.data

if __name__ == '__main__':
    unittest.main()
