#!/usr/bin/env python
from instagram.client import InstagramAPI

CODE = '57376554e9e8452e82538816e2629354'

CONFIG = {
    'client_id': '663798b919084fc7ac8c3e905e0b4381',
    'client_secret': '99f30eab3bd148a39345f9b2d2ff8971',
    'redirect_uri': 'http://yancao.me'
}

ACCESS_TOKEN = '531383149.663798b.d227d576320843839b577dd9eda5daa4'
MY_ID = 531383149
PMPM_ID = 231677378
scope = ['likes']

def get_auth():
    unauth_api = InstagramAPI(**CONFIG)
    redirect_uri = unauth_api.get_authorize_login_url(scope = scope)
    print "Visit this page and authorize access in your browser:\n", redirect_uri

def auth_request():
    #access_token, user_info = unauthenticated_api.exchange_code_for_access_token(CODE)
    api = InstagramAPI(access_token=ACCESS_TOKEN)
    recent_media, next = api.user_recent_media(user_id=39160400)
    for media in recent_media:
        #print media.id
        liked_user = []
        for user in api.media_likes(media.id):
            liked_user.append(user.username)
        if 'cyandterry' in liked_user:
            #api.like_media(media.id)
            api.unlike_media(media.id)
        #api.like_media(media.id)

if __name__ == '__main__':
    auth_request()

# TODO
# 1. Make Pagination work
# 2. Move out the config file and create .in file, register another app since this one is exposed to github
# 3. Regenerate access code and write it to config file. If access code invalid, go and get new one
# 4. After a successful like, send email with standard resolution photo.
# 5. Deploy this whole thing to web server.

# Little thing:
# 1. get user_id by username
