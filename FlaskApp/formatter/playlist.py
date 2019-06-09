from FlaskApp.formatter.datetime import to_datetime, from_datetime
from FlaskApp.formatter.track import format_simple_track
from FlaskApp.formatter.user import format_basic_user, format_simple_user
from FlaskApp.formatter.util import format_all

from datetime import datetime


def format_playlist_track(result):
    playlist_track = {
        'added_at': to_datetime(result['added_at'], 'second'),
        'added_by': format_basic_user(result['added_by']),
        'track': format_simple_track(result['track']),
        'type': 'playlist_track'}
    
    return playlist_track


def format_simple_playlist(result):
    playlist = {
        'name': result['name'],
        'id': result['id'],
        'type': result['type']}
    
    return playlist


def format_playlist(result):
    playlist = {
        'collaborative': result['collaborative'],
        'description': result['description'],
        'followers': result['followers']['total'],
        'name': result['name'],
        'owner': format_simple_user(result['owner']),
        'public': result['public'],
        'snapshot_id': result['snapshot_id'],
        'tracks': format_all(result['tracks'], format_playlist_track),
        'uri': result['uri'],
        'id': result['id'],
        'type': result['type']}

    return playlist
