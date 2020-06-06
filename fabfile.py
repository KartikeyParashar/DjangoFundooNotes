from fabric.api import local


def backup():
    local("git pull")
    local("git add .")
    print("Enter Your Commit Comment: ")
    comment = input()
    local("git commit -m '%s'" % comment)
    local("git push")


# Before using this function, use this command -> export DJANGO_SETTINGS_MODULE=FUNDOONOTES.settings
def celeryworker():
    local("celery -A FUNDOONOTES worker -l info")


# Before using this function, use this command -> export DJANGO_SETTINGS_MODULE=FUNDOONOTES.settings
def celerybeat():
    local("celery -A FUNDOONOTES beat -l info")


def docker_image():
    local("sudo docker images")


def docker_image_remove():
    print("Enter the image_id you want to stop forcefully")
    id = input()
    local("sudo docker rmi -f %s" % id)


def docker_start():
    local("sudo service docker start")


def docker_status():
    local("sudo service docker status")


def docker_stop():
    local("sudo service docker stop")


def docker_build():
    local("sudo docker-compose build")


def docker_run():
    local("sudo docker-compose up")


def status_redis():
    local("sudo systemctl status redis-server")


def start_redis():
    local("sudo systemctl start redis-server")


def stop_redis():
    local("sudo systemctl stop redis-server")


def status_rabbitmq():
    local("sudo systemctl status rabbitmq-server")


def start_rabbitmq():
    local("sudo systemctl start rabbitmq-server")


def stop_rabbitmq():
    local("sudo systemctl stop rabbitmq-server")


def show_docker_container():
    local("sudo docker ps -a")


def stop_docker_container():
    print("Enter the container_id you want to stop")
    id = input()
    local("sudo docker stop %s" % id)


def elasticsearch():
    local("python3 manage.py search_index --rebuild")


def elasticsearch_connection_status():
    local("sudo systemctl status elasticsearch.service")


def elasticsearch_connection_start():
    local("sudo systemctl start elasticsearch.service")


def elasticsearch_connection_stop():
    local("sudo systemctl stop elasticsearch.service")


def fuser():
    local("fuser -k 8000/tcp")


def makemigrations():
    local("python3 manage.py makemigrations")


def migrate():
    local("python3 manage.py migrate")


def runserver():
    local("python3 manage.py runserver")


def shell():
    local("python3 manage.py shell")