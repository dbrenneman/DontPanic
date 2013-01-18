from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm

env.hosts = ['davidbrenneman.com']


def test():
    with settings(warn_only=True):
        result = local('python dontpanic_tests.py', capture=True)
    if result.failed and not confirm("Tests failed. Continue anyway?"):
        abort("Aborting at user request.")


def deploy():
    test()
    code_dir = '/home/david/DontPanic'
    with settings(warn_only=True):
        if run("test -d %s" % code_dir).failed:
            run("git clone git://github.com/dbrenneman/DontPanic.git %s" % code_dir)
    with cd(code_dir):
        run("git pull")
        sudo("supervisorctl restart all")
