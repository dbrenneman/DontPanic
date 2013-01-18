from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm

env.hosts = ['blog@davidbrenneman.com']


def test():
    with settings(warn_only=True):
        result = local('./python dontpanic_test.py', capture=True)
    if result.failed and not confirm("Tests failed. Continue anyway?"):
        abort("Aborting at user request.")


def commit():
    local("git add -p && git commit")


def push():
    local("git push origin master")


def prepare_deploy():
    test()
    commit()
    push()


def deploy():
    code_dir = '/home/blog/DontPanic'
    with settings(warn_only=True):
        if run("test -d %s" % code_dir).failed:
            run("git clone github.com:/dbrenneman/DontPanic.git %s" % code_dir)
    with cd(code_dir):
        run("git pull")
        sudo("supervisorctl restart all")
