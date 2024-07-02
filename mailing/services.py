import smtplib
from datetime import datetime, timedelta

import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from django.conf import settings
from django.core.mail import send_mail

from mailing.models import Mailing, Log, Message
from django.core.cache import cache

from config.settings import CACHE_ENABLED


def send_mailing():
    """
    Функция отправки рассылок
    """
    zone = pytz.timezone(settings.TIME_ZONE)
    current_datetime = datetime.now(zone)
    mailings = Mailing.objects.filter(next_send_time__lte=current_datetime,
                                      status__in=[Mailing.STARTED, Mailing.CREATED])
    for mailing in mailings:
        mailing.status = Mailing.STARTED
        clients = mailing.clients.all()
        try:
            server_response = send_mail(
                subject=mailing.message.title,
                message=mailing.message.message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[client.email for client in clients],
                fail_silently=False,
            )
            Log.objects.create(status=Log.SUCCESS,
                               server_response=server_response,
                               mailing=mailing, )
        except smtplib.SMTPException as e:
            Log.objects.create(status=Log.FAIL,
                               server_response=str(e),
                               mailing=mailing, )

        if mailing.periodicity == 'Раз в день':
            mailing.next_send_time += timedelta(days=1)
        elif mailing.regularity == 'Раз в неделю':
            mailing.next_send_time += timedelta(weeks=1)
        elif mailing.regularity == 'Раз в месяц':
            mailing.next_send_time += timedelta(days=30)
        mailing.save()


def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_mailing, 'interval', seconds=10)

    if not scheduler.running:
        scheduler.start()


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
