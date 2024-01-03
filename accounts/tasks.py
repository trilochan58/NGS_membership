from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import HttpResponse

from celery import shared_task


# @shared_task(bind=True)
def send_token_mail(email, token):
    print("in sent funcion")
    subject = "Verify Your Account"
    message = f"Your pin is {token}. Login with your new account and enter this pin to verify."
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [
        email,
    ]
    print(recipient_list)
    send_mail(subject, message, email_from, recipient_list)
    return True


# @shared_task(bind=True)
def send_group_mail(subject, message, mail_list):
    subject = subject
    message = message
    email_from = settings.EMAIL_HOST_USER
    recipient_list = mail_list
    send_mail(subject, message, email_from, recipient_list)
    return True
