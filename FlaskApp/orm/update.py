from datetime import datetime
from functools import reduce

from pymongo.errors import DuplicateKeyError, WriteError

from FlaskApp import mongo, scheduler
from FlaskApp.orm.fetch import *
from FlaskApp.orm.find import find_playlist
from FlaskApp.orm.util import document_exists
from FlaskApp.orm.create import create_playlist


def update_recently_played(user_id):
    print(f'----- UPDATING RECENTLY PLAYED FOR {user_id} -----')

    recently_played = fetch_recently_played(user_id)

    if len(recently_played) > 0:
        print(f'{len(recently_played)} SONGS FOUND')
        try:
            mongo.db.recently_played.insert(recently_played)
        except DuplicateKeyError as e:
            print('ATTEMPTED TO INSERT DUPLICATE PLAY HISTORY')

    mongo.db.users.update_one(
        {'user.id': user_id},
        {'$currentDate': {'recently_played.last_checked': True}})
    
    update_tracks([ph['track'] for ph in recently_played])

    return recently_played


def update_playlist(playlist_id):
    print(f'----- UPDATING PLAYLIST {playlist_id} -----')

    db_playlist = find_playlist(playlist_id)

    if db_playlist is None:
        db_playlist = create_playlist(playlist_id)
        playlist = db_playlist['playlist']
    else:
        playlist = fetch_playlist(playlist_id)

    if any([db_playlist['playlist'][k] != playlist[k] for k in playlist.keys()]):
        time = datetime.utcnow()

        old_playlist = {
            'modified_at': time,
            'playlist': db_playlist['playlist']}

        created_at = db_playlist['created_at']
        if created_at is None and len(playlist['tracks']) > 0:
            created_at = min([track['added_at'] for track in playlist['tracks']])

        update = {
            '$addToSet': {'history': old_playlist},
            '$set': {
                'playlist': playlist,
                'last_modified': time,
                'created_at': created_at},
            '$currentDate': {'last_checked': True}}
    else:
        update = {
            '$currentDate': {'last_checked': True}}
    
    mongo.db.playlists.update_one({'playlist.id': playlist_id}, update)

    update_tracks([pt['track'] for pt in playlist['tracks']])

    return find_playlist(playlist_id)
    

def update_albums(albums):
    album_ids = list(set(filter(
        lambda id: not document_exists(mongo.db.albums, {'id': id}),
        [album['id'] for album in albums])))
    
    new_albums = []
    if len(album_ids) > 0:
        new_albums = fetch_albums(album_ids)

        try:
            mongo.db.albums.insert(new_albums)
        except DuplicateKeyError as e:
            print('ATTEMPTED TO INSERT DUPLICATE ALBUM')
        
        update_artists(reduce(lambda art, alb: art + alb['artists'], new_albums, []))
    
    return new_albums


def update_artists(artists):
    artist_ids = list(set(filter(
        lambda id: not document_exists(mongo.db.artists, {'id': id}),
        [artist['id'] for artist in artists])))
    
    new_artists = []
    if len(artist_ids) > 0:
        new_artists = fetch_artists(artist_ids)

        try:
            mongo.db.artists.insert(new_artists)
        except DuplicateKeyError as e:
            print('ATTEMPTED TO INSERT DUPLICATE ARTIST')
        
    return new_artists


def update_tracks(tracks):
    track_ids = list(set(filter(
        lambda id: not document_exists(mongo.db.tracks, {'id': id}),
        [track['id'] for track in tracks])))
    
    new_tracks = []
    if len(track_ids) > 0:
        new_tracks = fetch_tracks(track_ids)

        try:
            mongo.db.tracks.insert(new_tracks)
        except DuplicateKeyError as e:
            print('ATTEMPTED TO INSERT DUPLICATE TRACK')

        update_albums([track['album'] for track in new_tracks])
        update_artists(reduce(lambda art, trk: art + trk['artists'], new_tracks, []))
    
    return new_tracks
