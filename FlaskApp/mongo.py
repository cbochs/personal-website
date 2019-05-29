import json

from pymongo.errors import DuplicateKeyError
from FlaskApp import mongo
from FlaskApp.jsonencoder import JSONEncoder
from FlaskApp.spotify_api import Spotify


def setup_user(token_info):
    sp = Spotify(token_info['access_token'])
    me = sp.me()

    user = {
        'user_id': me['id'],
        'display_name': me['display_name'],
        **token_info}
    
    try:
        mongo.db.users.insert_one(user)
    except DuplicateKeyError as e:
        pass

    return user

def find_user(user_id):
    user = mongo.db.users.find_one({'user_id': user_id})
    return user