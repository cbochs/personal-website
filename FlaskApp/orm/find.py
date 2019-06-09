
from FlaskApp.orm.util import update_user
from FlaskApp import mongo


def find_user(user_id):
    user = mongo.db.users.find_one({'user.id': user_id})
    return update_user(user) if user else None


def find_playlist(playlist_id):
    return mongo.db.playlists.find_one({'playlist.id': playlist_id})
 