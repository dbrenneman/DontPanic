from . import db


class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, unique=True)
    slug = db.Column(db.Text, unique=True)
    body = db.Column(db.Text)
    published = db.Column(db.Text)
    updated = db.Column(db.Text)
