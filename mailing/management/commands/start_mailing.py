from apscheduler.schedulers.background import BackgroundScheduler

from mailing.services import send_mailing


# Функция старта периодических задач
def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_mailing, 'interval', seconds=10)
    scheduler.start()



import logging

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util

from distribution.tasks import daily_tasks, weekly_tasks, monthly_tasks


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            daily_tasks,
            trigger=CronTrigger(minute="*/1"),
            id="daily_job",
            max_instances=1,
            replace_existing=True,
        )

        scheduler.add_job(
            weekly_tasks,
            trigger=CronTrigger(day_of_week="*/1"),
            id="weekly_job",
            max_instances=1,
            replace_existing=True,
        )

        scheduler.add_job(
            monthly_tasks,
            trigger=CronTrigger(day="*/30"),
            id="monthly_job",
            max_instances=1,
            replace_existing=True,
        )

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
