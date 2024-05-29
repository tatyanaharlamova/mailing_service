from django.conf import settings
from django.core.mail import send_mail

from mailing.models import Client


def send_mailing(obj: Client):
    send_mail('Создан клиент',
              f'Новый клиент: {obj.name}, {obj.email}',
              settings.EMAIL_HOST_USER, ['ejik27@mail.ru'])

