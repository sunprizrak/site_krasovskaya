from celery import shared_task
from celery.utils.log import get_task_logger
import os
import markdown
import requests
from django.conf import settings
from instagrapi import Client
from django.core.files.base import ContentFile
from .models import NewsModel, Subscribe
from django.core.mail import send_mail

logger = get_task_logger(__name__)


@shared_task
def send_new_news_notification(new_news_ids):
    new_news = NewsModel.objects.filter(pk__in=new_news_ids)
    subscribers = Subscribe.objects.all()

    news_content = '\n\n'.join([f"{news.title}\n{news.text}" for news in new_news])
    subject = 'Последние новости'
    message = f"Привет!\n\nВот последние посты из нашего Instagram:\n\n{news_content}\n\nС уважением, Команда"
    from_email = settings.EMAIL_HOST_USER

    for subscriber in subscribers:
        message = f'Привет, {subscriber.name}!\n\nВот последние новости:\n\n{news_content}\n\nС уважением, Екатерина Красовская'
        send_mail(subject, message, from_email, [subscriber.email])


@shared_task
def fetch_instagram_news():
    logger.info('Fetching Instagram news...')

    ACCOUNT_USERNAME = os.environ.get('ACCOUNT_USERNAME')
    ACCOUNT_PASSWORD = os.environ.get('ACCOUNT_PASSWORD')

    if settings.DEBUG:
        cl = Client(delay_range=[1, 3])
    else:
        PROXY_USERNAME = os.environ.get('PROXY_USERNAME')
        PROXY_PASSWORD = os.environ.get('PROXY_PASSWORD')
        PROXY_HOST = os.environ.get('PROXY_HOST')
        PROXY_PORT = os.environ.get('PROXY_PORT')

        proxy_url = f"http://{PROXY_USERNAME}:{PROXY_PASSWORD}@{PROXY_HOST}:{PROXY_PORT}"

        cl = Client(proxy=proxy_url, delay_range=[1, 3])

    cl.login(ACCOUNT_USERNAME, ACCOUNT_PASSWORD)

    user_id = cl.user_id_from_username(ACCOUNT_USERNAME)
    medias = cl.user_medias(user_id, 3)

    new_news = []

    if medias:
        for index, media in enumerate(medias):
            instagram_id = media.id
            title = media.caption_text.strip().split('\n')[0]
            text = markdown.markdown('<br>'.join(media.caption_text.strip().split('\n')[2:]))
            taken_at = media.taken_at
            img_url = str(media.thumbnail_url)

            response = requests.get(img_url)

            if response.status_code == 200:
                image_content = ContentFile(response.content)
                image_name = img_url.split('/')[-1].split('?')[0]

                news_item, created = NewsModel.objects.update_or_create(
                    instagram_id=instagram_id,
                    defaults={
                        'title': title,
                        'text': text,
                        'taken_at': taken_at,
                    }
                )

                if created:
                    news_item.image.save(image_name, image_content)
                    new_news.append(news_item)
                else:
                    news_item.image.save(image_name, image_content)
                    news_item.save()

        news_count = NewsModel.objects.count()

        if news_count > 3:
            # Удаление старых новостей
            medias_ids = [media.id for media in medias]
            news = NewsModel.objects.all()

            for news_item in news:
                if news_item.instagram_id not in medias_ids:
                    news_item.delete()

        logger.info('Instagram news fetched and processed successfully.')
    else:
        logger.warning('No Instagram news found.')

    if new_news:
        new_news_ids = [news.pk for news in new_news]
        send_new_news_notification.delay(new_news_ids)
