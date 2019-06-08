from functools import reduce
from datetime import datetime

from FlaskApp import mongo
from FlaskApp.orm.fetch import *
from FlaskApp.orm.find import find_user
from FlaskApp.orm.util import document_exists
from pymongo.errors import DuplicateKeyError
from FlaskApp.formatter.datetime import to_datetime, from_datetime


def update_recently_played(user_id):
    print('----- HELLO I AM AN UPDATE -----')

    recently_played = fetch_recently_played(user_id)

    try:
        mongo.db.recently_played.insert(recently_played)
    except DuplicateKeyError as e:
        print('ATTEMPTED TO INSERT DUPLICATE PLAY HISTORY')

    mongo.db.users.update_one(
        {'user_info.id': user_id},
        {'$set': {'recently_played.last_checked': datetime.utcnow()}})
    
    update_tracks([ph['track'] for ph in recently_played])
    
    return recently_played


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
