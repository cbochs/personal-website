from datetime import datetime
from functools import reduce

from FlaskApp import mongo, oauth
from FlaskApp.formatter import *
from FlaskApp.spotify.api import Spotify, SpotifyOAuth
from pymongo.errors import DuplicateKeyError


def create_user(token_info):
    token_info = oauth.refresh_access_token(token_info)
    sp = Spotify(token_info['access_token'])
    user = format_user(sp.me(), token_info)

    return user


def is_token_expired(token_info):
    time = datetime.utcnow().timestamp()
    return (token_info['expires_at'] - time) < 60


def update_token_info(user):
    if is_token_expired(user['token_info']):
        token_info = oauth.refresh_access_token(user['token_info'])
    else:
        token_info = user['token_info']

    user['token_info'] = token_info
    mongo.db.test.update_one({'id': user['id']}, {'$set': user})

    return user


def update_recently_played(user):
    user = update_token_info(user)

    sp = Spotify(user['token_info']['access_token'])
    rp = sp.recently_played(limit=50)['items']
    rp = format_all(rp, format_play_history, user=format_simple_user(user))

    try:
        mongo.db.recently_played.insert(rp)
    except DuplicateKeyError as e:
        print('ATTEMPTED TO INSERT DUPLICATE PLAY HISTORY')


    tracks = [ph['track'] for ph in rp]
    tracks = update_tracks(tracks)

    albums = [t['album'] for t in tracks]
    albums = update_albums(albums)

    artists = reduce(lambda art, trk: art + trk['artists'], tracks, []) \
              + reduce(lambda art, alb: art + alb['artists'], albums, [])
    artists = update_artists(artists)


def update_artists(artists):
    user = mongo.db.test.find_one({'id': 'notbobbobby'})
    user = update_token_info(user)

    unique_filter = lambda id: not document_exists(mongo.db.artists, {'id': id}, {'id': 1})

    artist_ids = [a['id'] for a in artists]
    artist_ids = list(set(filter(unique_filter, artist_ids)))


    if len(artist_ids) > 0:
        sp = Spotify(user['token_info']['access_token'])
        artists = []
        for ids in chunks(artist_ids, 50):
            artists.extend(sp.artists(ids=','.join(ids))['artists'])
        artists = format_all(artists, format_artist)

        try:
            mongo.db.artists.insert(artists)
        except DuplicateKeyError as e:
            print('ATTEMPTED TO INSERT DUPLICATE ARTISTS')
    else:
        artists = []

    return artists


def update_albums(albums):
    user = mongo.db.test.find_one({'id': 'notbobbobby'})
    user = update_token_info(user)

    unique_filter = lambda id: not document_exists(mongo.db.albums, {'id': id}, {'id': 1})

    album_ids = [a['id'] for a in albums]
    album_ids = list(set(filter(unique_filter, album_ids)))

    if len(album_ids) > 0:
        sp = Spotify(user['token_info']['access_token'])
        albums = []
        for ids in chunks(album_ids, 20):
            albums.extend(sp.albums(ids=','.join(ids))['albums'])
        albums = format_all(albums, format_album)

        try:
            mongo.db.albums.insert(albums)
        except DuplicateKeyError as e:
            print('ATTEMPTED TO INSERT DUPLICATE ALBUMS')
    else:
        albums = []

    return albums


def update_tracks(tracks):
    user = mongo.db.test.find_one({'id': 'notbobbobby'})
    user = update_token_info(user)

    unique_filter = lambda id: not document_exists(mongo.db.tracks, {'id': id}, {'id': 1})

    track_ids = [t['id'] for t in tracks]
    track_ids = list(set(filter(unique_filter, track_ids)))

    if len(track_ids) > 0:
        sp = Spotify(user['token_info']['access_token'])
        tracks = []
        for ids in chunks(track_ids, 50):
            tracks.extend(sp.tracks(ids=','.join(ids))['tracks'])
        tracks = format_all(tracks, format_track)

        try:
            mongo.db.tracks.insert(tracks)
        except DuplicateKeyError as e:
            print('ATTEMPTED TO INSERT DUPLICATE TRACKS')
    else:
        tracks = []

    return tracks


def chunks(list_, n):
    for i in range(0, len(list_), n):
        yield list_[i:i+n]


def document_exists(collection, query, projection):
    return collection.find(query, projection) \
                     .limit(1) \
                     .count(with_limit_and_skip=True) > 0
