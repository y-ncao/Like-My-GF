#!/usr/bin/env python

from instagram.client import InstagramAPI
from ConfigParser import SafeConfigParser
import argparse
import datetime
import logging

config_parser = SafeConfigParser()
config_parser.read('config')

arg_parser = argparse.ArgumentParser(description='Auto-like my GF\'s Instagram')
arg_parser.add_argument('-v', '--verbose', action='store_true', help='Increase output verbosity')
args = arg_parser.parse_args()

CONFIG = dict( client_id     = config_parser.get('Client', 'client_id'),
               client_secret = config_parser.get('Client', 'client_secret'),
               redirect_uri  = config_parser.get('Client', 'redirect_uri'),
                 )
OTHER = dict( scope        = ['likes'],
              access_token = config_parser.get('Access Token', 'access_token'),
              target       = config_parser.get('Target', 'username'),
              log_path     = config_parser.get('Path', 'log_path')+'like_my_gf.log',
    )

if args.verbose:
    logging.basicConfig(filename=OTHER['log_path'], level=logging.DEBUG)
else:
    logging.basicConfig(filename=OTHER['log_path'], level=logging.INFO)


def get_auth():
    unauth_api = InstagramAPI(**CONFIG)
    redirect_uri = unauth_api.get_authorize_login_url(scope = OTHER['scope'])

    print "Visit this page and authorize access in your browser:\n", redirect_uri
    code = raw_input('Please type in the access code you got\n')
    OTHER['access_token'], me = unauth_api.exchange_code_for_access_token(code)

    with open('config', 'w') as cf:
        config_parser.set('Access Token', 'access_token', OTHER['access_token'])
        config_parser.write(cf)

def auth_request():
    api = InstagramAPI(access_token=OTHER['access_token'])
    target_ids = api.user_search(OTHER['target'])

    target_id = None
    for search_hit in target_ids:
        if search_hit.username == OTHER['target']:
            target_id = search_hit.id
            break

    if target_id == None:
        logging.error('Did not find user, please check username')
        return []

    my_name   = api.user().username
    logging.debug('Starting check recent media')
    recent_media, url = api.user_recent_media(user_id=target_id, count = 20)
    liked_media = []
    for media in recent_media:
        logging.debug('Processing media %s' % media.id)
        users = api.media_likes(media.id)
        will_like = True
        for user in users:
            if user.username == my_name:
                will_like = False
                break
        if will_like:
            logging.debug('Liking media %s' % media.id)
            api.like_media(media.id)
            liked_media.append(media)
        else:
            logging.debug('Already liked media %s, aborting like' % media.id)

    return liked_media

if __name__ == '__main__':
    if OTHER['access_token'] == 'None':           # Not mistake, but default token is 'None' but not None
        get_auth()
    liked_media = auth_request()
    if len(liked_media) > 0:
        logging.info('-'*10+str(datetime.datetime.now())+'-'*10)
        logging.info('-'*10+'Liked '+str(len(liked_media))+' medias'+'-'*10)

# TODO
# 1. Send email
