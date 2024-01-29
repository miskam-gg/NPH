from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from .models import Subscription, Post


@shared_task
def send_weekly_digest():
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