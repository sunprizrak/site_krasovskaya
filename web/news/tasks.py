from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings
from .models import NewsModel, Subscribe
from django.core.mail import send_mail

logger = get_task_logger(__name__)


@shared_task
def send_new_news_notification(new_news_ids):
    new_news = NewsModel.objects.filter(pk__in=new_news_ids)
    subscribers = Subscribe.objects.all()

    news_content = '\n\n'.join([f"{news.title}\n{news.text}" for news in new_news])
    subject = 'Последние новости'
    from_email = settings.EMAIL_HOST_USER

    for subscriber in subscribers:
        try:
            message = f'Привет, {subscriber.name}!\n\nВот последние новости:\n\n{news_content}\n\nС уважением, команда {settings.SITE_NAME}'
            send_mail(subject, message, from_email, [subscriber.email])
        except Exception as error:
            logger.error(f"Failed to send email to {subscriber.email}: {str(error)}")
            raise error


@shared_task
def check_and_send_new_news():
    new_news = NewsModel.objects.filter(is_sent=False)

    if new_news.exists():
        new_news_ids = list(new_news.values_list('id', flat=True))
        try:
            send_new_news_notification(new_news_ids)
            new_news.update(is_sent=True)
        except Exception as error:
            logger.error(f"Error during sending news notifications: {str(error)}")

