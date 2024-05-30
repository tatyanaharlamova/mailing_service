from smtplib import SMTPException

from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone


from mailing.models import Mailing, Log


def send_mailing(mailing):
    now = timezone.localtime(timezone.now())
    if mailing.start_date <= now <= mailing.end_date:
        for message in mailing.messages.all():
            for client in mailing.clients.all():
                try:
                    result = send_mail(
                        subject=message.title,
                        message=message.message,
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[client.email],
                        fail_silently=False
                    )
                    log = Log.objects.create(
                        time=mailing.start_time,
                        status=result,
                        server_response='OK',
                        mailing=mailing,
                        client=client
                    )
                    log.save()
                    return log
                except SMTPException as error:
                    log = Log.objects.create(
                        time=mailing.start_time,
                        status=False,
                        server_response=error,
                        mailing=mailing,
                        client=client
                    )
                    log.save()
                return log
    else:
        mailing.status = Mailing.COMPLETED
        mailing.save()


# m = Mailing.objects.get(id=1)
# send_mailing(m)
