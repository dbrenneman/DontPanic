from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'dontpanic.sqlite')

app = Flask(__name__)
db = SQLAlchemy(app)

from . import views, models

if __name__ == '__main__':
    app.run()
