from instagrapi import Client
import os

ACCOUNT_USERNAME = os.environ.get('ACCOUNT_USERNAME')
ACCOUNT_PASSWORD = os.environ.get('ACCOUNT_PASSWORD')


with open('.env.dev') as file:
    for line in file:
        if 'ACCOUNT_USERNAME' in line:
            ACCOUNT_USERNAME = line.split('=')[1].strip()
        elif 'ACCOUNT_PASSWORD' in line:
            ACCOUNT_PASSWORD = line.split('=')[1].strip()


cl = Client()
cl.login(ACCOUNT_USERNAME, ACCOUNT_PASSWORD)

user_id = cl.user_id_from_username(ACCOUNT_USERNAME)
medias = cl.user_medias(user_id, 1)
print(medias)
print(medias[0].thumbnail_url)
