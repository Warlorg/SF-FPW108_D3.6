import datetime

from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from .models import Post, Category


@shared_task
def weekly_notifications():
	today = datetime.datetime.now()
	last_week = today - datetime.timedelta(days=7)
	posts = Post.objects.filter(dateCreation__gte=last_week)
	categories = set(posts.values_list('postCategory__name', flat=True))
	subscribers = set(Category.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))

	html_content = render_to_string(
		'weekly_mailing.html',
		{
			'link': settings.SITE_URL,
			'posts': posts
		}
	)
	msg = EmailMultiAlternatives(
		subject='Статьи за неделю.',
		body='',
		from_email=settings.DEFAULT_FROM_EMAIL,
		to=subscribers,
	)
	msg.attach_alternative(html_content, 'text/html')
	msg.send()

@shared_task
def new_post_notification(instance_id):
	instance = Post.objects.get(pk=instance_id)
	categories = instance.postCategory.all()
	subscribers = []

	for cat in categories:
		subscribers += cat.subscribers.all()

	subscribers_emails = list(set([s.email for s in subscribers]))
	print(subscribers_emails)

	for email in subscribers_emails:
		html_content = render_to_string(
			'post_created_email.html',
			{
				'text': instance.preview,
				'link': f'{settings.SITE_URL}/news/{instance_id}'
			}
		)
		msg = EmailMultiAlternatives(
			subject=instance.title,
			body='',
			from_email=settings.DEFAULT_FROM_EMAIL,
			to=[email],
		)
		msg.attach_alternative(html_content, 'text/html')
		msg.send()
