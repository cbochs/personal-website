from FlaskApp import mongo
from FlaskApp.orm.fetch import fetch_user, fetch_playlist
from FlaskApp.orm.util import document_exists
from pymongo.errors import DuplicateKeyError


def create_user(token_info):
    user_info = fetch_user(token_info)

    user = {
        'token_info': token_info,
        'recently_played': {
            'active': True,
            'last_checked': None},
        'playlists': {
            'watched': []},
        'user': user_info}
    
    user_id = user_info['id']

    if not document_exists(mongo.db.users, {'user.id': user_id}):
        try:
            mongo.db.users.insert_one(user)
        except DuplicateKeyError as e:
            print('ATTEMPTED TO INSERT DUPLICATE USER')
    
    return user


def create_playlist(playlist_id, created_for=None):
    playlist_info = fetch_playlist(playlist_id)

    created_at = None
    if len(playlist_info['tracks']) > 0:
        created_at = min([track['added_at'] for track in playlist_info['tracks']])

    playlist = {
        'created_at': created_at,
        'created_for': created_for,
        'history': [],
        'last_checked': None,
        'last_modified': None,
        'playlist': playlist_info}

    if not document_exists(mongo.db.playlists, {'playlist.id': playlist_id}):
        try:
            mongo.db.playlists.insert_one(playlist)
        except DuplicateKeyError as e:
            print('ATTEMPTED TO INSERT DUPLICATE PLAYLIST')

    return playlist