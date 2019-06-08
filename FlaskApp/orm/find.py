
from FlaskApp.orm.util import update_user
from FlaskApp import mongo


def find_user(user_id):
    return update_user(mongo.db.users.find_one({'user_info.id': user_id}))


def find_playlist(playlist_id):
    return mongo.db.users.find_one({'id': playlist_id})
 