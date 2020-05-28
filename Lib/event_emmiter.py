from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from pymitter import EventEmitter


email_event = EventEmitter()


@email_event.on("Account_Activate_Event")
def email_for_activating_account(message, recipient_list):
    """

    :param message: Here we pass a message, that we have to send to mail
    :param recipient_list: Here we pass receiver to whom, we want to send email
    :return: Function send the mail
    """
    email_from = settings.EMAIL_HOST_USER
    subject = "Thank You for Registering to OUR SITE"
    msg = EmailMultiAlternatives(subject=subject, from_email=email_from, to=recipient_list, body=message)
    msg.attach_alternative(message, "text/html")
    msg.send()


@email_event.on("Reset_Password_Event")
def email_for_reset_password(message, recipient_list):
    """

    :param message: Here we pass a message, that we have to send to mail
    :param recipient_list: Here we pass user email who want to send the email
    :return: Function send the mail
    """
    email_from = settings.EMAIL_HOST_USER
    subject = "Link for Reset the PASSWORD"
    msg = EmailMultiAlternatives(subject=subject, from_email=email_from, to=recipient_list, body=message)
    msg.attach_alternative(message, "text/html")
    msg.send()


@email_event.on("reminder_event")
def email_for_reminder_mail(message, recipient_list):
    """
    :param message: here we passing message for mail
    :param recipient_list: here we passing receiver mail
    :return:this function send the email
    """
    email_from = settings.EMAIL_HOST_USER
    subject = 'Reminder for You from Fundoo'
    # send_mail(subject, message, email_from, recipient_list)
    msg = EmailMultiAlternatives(subject=subject, from_email=email_from,
                                 to=recipient_list, body=message)
    msg.attach_alternative(message, "text/html")
    msg.send()
