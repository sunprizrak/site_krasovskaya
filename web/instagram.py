import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')
django.setup()
import markdown
import requests
import logging
from instagrapi import Client
from django.core.files.base import ContentFile
from news.models import NewsModel

logger = logging.getLogger()

ACCOUNT_USERNAME = os.environ.get('ACCOUNT_USERNAME')
ACCOUNT_PASSWORD = os.environ.get('ACCOUNT_PASSWORD')

# if not ACCOUNT_USERNAME and not ACCOUNT_PASSWORD:
#     with open('.env.dev') as file:
#         for line in file:
#             if 'ACCOUNT_USERNAME' in line:
#                 ACCOUNT_USERNAME = line.split('=')[1].strip()
#             elif 'ACCOUNT_PASSWORD' in line:
#                 ACCOUNT_PASSWORD = line.split('=')[1].strip()


cl = Client()
cl.login(ACCOUNT_USERNAME, ACCOUNT_PASSWORD)

user_id = cl.user_id_from_username(ACCOUNT_USERNAME)
medias = cl.user_medias(user_id, 3)

if medias:
    news = NewsModel.objects.all()

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

            if not created:
                news_item.image.save(image_name, image_content)
                news_item.save()
            else:
                news_item.image.save(image_name, image_content)

    news_count = NewsModel.objects.count()

    if news_count > 3:
        medias_ids = [media.id for media in medias]
        news = NewsModel.objects.all()

        for news_item in news:
            if news_item.instagram_id not in medias_ids:
                news_item.delete()

