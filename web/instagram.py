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
from instagrapi.exceptions import LoginRequired

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
session_path = 'session.json'

if os.path.exists(session_path):
    session = cl.load_settings(session_path)

    login_via_session = False
    login_via_pw = False

    if session:
        try:
            cl.set_settings(session)
            cl.login(ACCOUNT_USERNAME, ACCOUNT_PASSWORD)

            # check if session is valid
            try:
                cl.get_timeline_feed()
            except LoginRequired:
                logger.info("Session is invalid, need to login via username and password")

                old_session = cl.get_settings()

                # use the same device uuids across logins
                cl.set_settings({})
                cl.set_uuids(old_session["uuids"])

                cl.login(ACCOUNT_USERNAME, ACCOUNT_PASSWORD)
            login_via_session = True
        except Exception as e:
            logger.info("Couldn't login user using session information: %s" % e)

    if not login_via_session:
        try:
            logger.info("Attempting to login via username and password. username: %s" % ACCOUNT_USERNAME)
            if cl.login(ACCOUNT_USERNAME, ACCOUNT_PASSWORD):
                login_via_pw = True
        except Exception as e:
            logger.info("Couldn't login user using username and password: %s" % e)

    if not login_via_pw and not login_via_session:
        raise Exception("Couldn't login user with either password or session")

else:
    cl.login(ACCOUNT_USERNAME, ACCOUNT_PASSWORD)
    cl.dump_settings(session_path)


user_id = cl.user_id_from_username(ACCOUNT_USERNAME)
medias = cl.user_medias(user_id, 3)

if medias:
    news = NewsModel.objects.all()

    for index, media in enumerate(medias):
        title = media.caption_text.strip().split('\n')[0]
        text = markdown.markdown('<br>'.join(media.caption_text.strip().split('\n')[2:]))
        img_url = str(media.thumbnail_url)

        response = requests.get(img_url)

        if response.status_code == 200:
            image_content = ContentFile(response.content)
            image_name = img_url.split('/')[-1].split('?')[0]

            if len(news) == len(medias):
                news[index].title = title
                news[index].image.save(image_name, image_content)
                news[index].text = text
                news[index].save()
            else:
                obj = NewsModel(
                    title=title,
                    text=text,
                )
                obj.image.save(image_name, image_content)
                obj.save()




