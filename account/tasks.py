# from celery.app import task
from celery import app
from celery.app import task
from django.core.mail import send_mail

from home_accounting import settings


@task
def send_mail_task(email, username):
    subject = f"Регистрация на сайте 'Личная Бухгалтерия'"
    message = f"Поздравляем, {username}! \nВы зарегистрированы!"
    send_mail(subject, message, settings.EMAIL_HOST_USER, [email])
