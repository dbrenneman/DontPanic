import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()
CHANGES = open(os.path.join(here, 'CHANGES.rst')).read()

requires = [
    'Flask',
    'Flask-SqlAlchemy',
    ]

setup(name='DontPanic',
      version='0.0',
      description='DontPanic',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Flask",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='David Brenneman',
      author_email='db@davidbrenneman.com',
      url='https://github.com/dbrenneman/DontPanic',
      keywords='web wsgi flask',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='dontpanic',
      install_requires=requires,
      entry_points="""""",
      )
