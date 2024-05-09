from instagrapi import Client

ACCOUNT_USERNAME = 'sunprizrak'
ACCOUNT_PASSWORD = 'test_API'

cl = Client()
cl.login(ACCOUNT_USERNAME, ACCOUNT_PASSWORD)

user_id = cl.user_id_from_username(ACCOUNT_USERNAME)
medias = cl.user_medias(user_id, 1)
print(medias)
print(len(medias))
print(dir(medias[0]))
raw = medias[0].parse_raw()
print(raw)
