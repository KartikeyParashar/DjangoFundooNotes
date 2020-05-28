import django
django.setup()

from celery.decorators import task
from users.models import Fundoo
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from Lib.event_emmiter import email_event
from .models import Note
from django.utils import timezone


def task_send_email_for_reminder(user_id, title, pk):
    """
    :param user_id:here we get user id for getting appropriate user
    :param title:here we gate title of note
    :param pk:here we get id of note
    :return:this function is called when any reminder match and sens mail for reminder
    """
    user = Fundoo.objects.get(pk=user_id)
    # mimicking a long running process
    current_site = Site.objects.get_current()

    message = render_to_string('fundoonotes/note_template.html', {
        'name': user.username,
        'title': title,
        'domain': current_site.domain,
        'note_id': pk
    })

    recipient_list = [user.email, ]
    email_event.emit("reminder_event", message, recipient_list)


@task(name='sending email for reminder')
def send_reminder():
    """
    :return:this function is used for checking reminder every 1 minute
    """
    reminder_notes_list = Note.objects.filter(reminder__isnull=False)
    status = "No Received Task"
    for num in range(len(reminder_notes_list)):
        nextTime = timezone.now() + timezone.timedelta(minutes=1)
        # status = "No Received Task"
        if timezone.now() <= reminder_notes_list.values()[num]["reminder"] <= nextTime:
            task_send_email_for_reminder(reminder_notes_list.values()[num]["user_id"],
                                         reminder_notes_list.values()[num]["title"],
                                         reminder_notes_list.values()[num]["id"])
            status = "Received Task,Successfully Send Mail"

    return status
