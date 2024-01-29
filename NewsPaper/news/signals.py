from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
from .models import Post, Category, Subscription

@receiver(post_save, sender=User)
def add_user_to_common_group(sender, instance, created, **kwargs):
    if created:
        common_group = Group.objects.get(name='common')
        instance.groups.add(common_group)


@receiver(post_save, sender=get_user_model())
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        subject = 'Добро пожаловать на News Portal!'
        context = {
            'username': instance.username,
        }
        message = render_to_string('news/welcome_email.html', context)
        plain_message = strip_tags(message)
        send_mail(subject, plain_message, 'ваш_email@gmail.com', [instance.email], html_message=message)

@receiver(m2m_changed, sender=Subscription.categories.through)
def subscribe_user_to_category(sender, instance, action, **kwargs):
    if action == 'post_add':
        user = instance.user
        category = instance.category
        if user.email:
            subject = f'Вы подписались на категорию "{category}"'
            message = f'Вы успешно подписались на категорию "{category}".'
            send_mail(subject, message, 'ваш_email@gmail.com', [user.email])

@receiver(post_save, sender=Post)
def send_new_article_notification(sender, instance, **kwargs):
    categories = instance.categories.all()
    for category in categories:
        subscribers = Subscription.objects.filter(category=category)
        for subscriber in subscribers:
            user = subscriber.user
            if user.email:
                subject = f'Новая статья в категории "{category}"'
                context = {
                    'article_title': instance.title,
                    'article_link': reverse('news:article_detail', args=[instance.pk]),
                }
                message = render_to_string('news/new_article_email.html', context)
                plain_message = strip_tags(message)
                send_mail(subject, plain_message, 'ваш_email@gmail.com', [user.email], html_message=message)