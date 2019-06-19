from datetime import datetime

import pymongo
from FlaskApp import mongo
from FlaskApp.orm.util import update_user


def find_user(user_id):
    user = mongo.db.users.find_one({'user.id': user_id})
    return update_user(user) if user else None


def find_recently_played(user_id, start_time=None, end_time=None):
    query = {'user.id': user_id}

    if start_time or end_time:
        query['played_at'] = {}
        if start_time is not None:
            query['played_at']['$gt'] = datetime.utcfromtimestamp(start_time)
        if end_time is not None:
            query['played_at']['$lt'] = datetime.utcfromtimestamp(end_time)

    result = mongo.db.recently_played.find(query) \
                                     .sort('played_at', pymongo.DESCENDING)

    return [rp for rp in result]


def find_playlist(playlist_id):
    return mongo.db.playlists.find_one({'playlist.id': playlist_id})
