import logging
from django.conf import settings
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from news.models import Post, Subscription

logger = logging.getLogger(__name__)

def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)

def my_job():
    today = datetime.now()
    week_ago = today - timedelta(days=7)
    new_articles = Post.objects.filter(created_at__gte=week_ago)

    for user in User.objects.all():
        subscriptions = Subscription.objects.filter(user=user)
        categories = [subscription.category for subscription in subscriptions]
        user_articles = new_articles.filter(categories__in=categories).distinct()

        if user_articles:
            subject = 'Еженедельный дайджест новых статей'
            context = {
                'user_articles': user_articles,
            }
            message = render_to_string('news/weekly_digest_email.html', context)
            plain_message = strip_tags(message)
            send_mail(subject, plain_message, 'ваш_email@gmail.com', [user.email], html_message=message)

class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(second="*/10"),  # То же, что и интервал, но задача тригера таким образом более понятна django
            id="my_job",  # уникальный айди
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")