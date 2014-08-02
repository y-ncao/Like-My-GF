#!/usr/bin/env python
from instagram.client import InstagramAPI
from ConfigParser import SafeConfigParser
import requests
import time
import logging

config_parser = SafeConfigParser()
config_parser.read('config')

CODE = '57376554e9e8452e82538816e2629354'
#ACCESS_TOKEN = '531383149.663798b.d227d576320843839b577dd9eda5daa4'
ACCESS_TOKEN = 'None'
CONFIG = dict(   client_id     = config_parser.get('Client', 'client_id'),
                 client_secret = config_parser.get('Client', 'client_secret'),
                 redirect_uri  = config_parser.get('Client', 'redirect_uri'),
                 )
Other = dict( scope        = ['likes'],
              access_token = config_parser.get('Access Token', 'access_token'),
              target       = config_parser.get('Target', 'username'),
    )

#unauth_api.user_search(target_username, 1)[0].id
MY_ID = 531383149
PMPM_ID = 231677378
print type(config_parser.get('Access Token', 'access_token'))

def get_auth():
    unauth_api = InstagramAPI(**CONFIG)
    redirect_uri = unauth_api.get_authorize_login_url(scope = Other['scope'])
    print "Visit this page and authorize access in your browser:\n", redirect_uri
    Other['access_token'] = raw_input('Please type in the access code you got\n')
    with open('config', 'w') as cf:
        config_parser.set('Access Token', 'access_token', Other['access_token'])
        config_parser.write(cf)


def auth_request():
    #access_token, user_info = unauthenticated_api.exchange_code_for_access_token(CODE)
    api = InstagramAPI(access_token=ACCESS_TOKEN)
    recent_media, url = api.user_recent_media(user_id=PMPM_ID, count = 20)
    for media in recent_media:
        print 'Processing media %s' % media.id
        liked_user = []
        users = api.media_likes(media.id)
        for user in users:
            liked_user.append(user.username)
        if 'cyandterry' not in liked_user:
            print 'Liking media %s' % media.id
            api.like_media(media.id)
        else:
            print 'Already liked media %s, aborting like' % media.id


if __name__ == '__main__':
    if Other['access_token'] == 'None':           # Not mistake, but default token is 'None' but not None
        get_auth()

    #auth_request()

# TODO
# 1. Make Pagination work
# 2. Move out the config file and create .in file, register another app since this one is exposed to github
# 3. Regenerate access code and write it to config file. If access code invalid, go and get new one
# 4. After a successful like, send email with standard resolution photo.
# 5. Deploy this whole thing to web server.

# Little thing:
# 1. get user_id by username
