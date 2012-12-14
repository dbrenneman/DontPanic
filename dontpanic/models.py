from sqlalchemy import (
    Column,
    Integer,
    Text,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class Article(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True)
    title = Column(Text, unique=True)
    slug = Column(Text, unique=True)
    body = Column(Text)
    published = Column(Text)
    updated = Column(Text)

    def __init__(self, title, body):
        self.title = title
        self.body = body
