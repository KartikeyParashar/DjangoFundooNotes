from fabric.api import local


def runserver():
    local("python3 manage.py runserver")


def fuser():
    local("fuser -k 8000/tcp")


def elasticsearch():
    local("python3 manage.py search_index --rebuild")


def backup():
    local("git pull")
    local("git add .")
    comment = input("Enter Your Commit Comment: ")
    local("git commit -m '%s'" % comment)
    local("git push")
