from fabric.api import local


def backup():
    local("git pull")
    local("git add .")
    print("Enter Your Commit Comment: ")
    comment = raw_input()
    local("git commit -m '%s'" % comment)
    local("git push")


# Before using this function, use this command -> export DJANGO_SETTINGS_MODULE=FUNDOONOTES.settings
def celeryworker():
    local("celery -A FUNDOONOTES worker -l info")


# Before using this function, use this command -> export DJANGO_SETTINGS_MODULE=FUNDOONOTES.settings
def celerybeat():
    local("celery -A FUNDOONOTES beat -l info")


def elasticsearch():
    local("python3 manage.py search_index --rebuild")


def fuser():
    local("fuser -k 8000/tcp")


def makemigrations():
    local("python3 manage.py makemigrations")


def migrate():
    local("python3 manage.py migrate")


def runserver():
    local("python3 manage.py runserver")