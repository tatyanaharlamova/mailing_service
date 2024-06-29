from smtplib import SMTPException
import os
import django
from django.core.cache import cache

from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

from config.settings import CACHE_ENABLED
from mailing.models import Mailing, Log, Message

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()


# def send_mailing(mailing):
#     now = timezone.localtime(timezone.now())
#     if mailing.start_date <= now <= mailing.end_date:
#         for message in mailing.messages.all():
#             for client in mailing.clients.all():
#                 try:
#                     result = send_mail(
#                         subject=message.title,
#                         message=message.message,
#                         from_email=settings.EMAIL_HOST_USER,
#                         recipient_list=[client.email],
#                         fail_silently=False
#                     )
#                     log = Log.objects.create(
#                         time=mailing.start_time,
#                         status=result,
#                         server_response='OK',
#                         mailing=mailing,
#                         client=client
#                     )
#                     log.save()
#                     return log
#                 except SMTPException as error:
#                     log = Log.objects.create(
#                         time=mailing.start_time,
#                         status=False,
#                         server_response=error,
#                         mailing=mailing,
#                         client=client
#                     )
#                     log.save()
#                 return log
#     else:
#         mailing.status = Mailing.COMPLETED
#         mailing.save()

#
# m = Mailing.objects.get(id=1)
# send_mailing(m)


def get_messages_from_cache():
    """
    Получение списка сообщений из кэша. Если кэш пуст,то получение из БД.
    """
    if not CACHE_ENABLED:
        return Message.objects.all()
    else:
        key = 'categories_list'
        messages = cache.get(key)
        if messages is not None:
            return messages
        else:
            messages = Message.objects.all()
            cache.set(key, messages)
            return messages
