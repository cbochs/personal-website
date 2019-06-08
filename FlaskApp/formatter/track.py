from FlaskApp.formatter.album import format_simple_album
from FlaskApp.formatter.artist import format_simple_artist
from FlaskApp.formatter.util import format_all


def format_simple_track(result):
    if result['is_local']:
        return None
    
    track = {
        'album': format_simple_album(result['album']),
        'artists': format_all(result['artists'], format_simple_artist),
        'name': result['name'],
        'id': result['id'],
        'type': result['type']}

    return track


def format_track(result):
    if result['is_local']:
        print(f'SKIPPING TRACK BECAUSE IT IS LOCAL {result["name"]}')
        return None

    track = {
        'album': format_simple_album(result['album']),
        'artists': format_all(result['artists'], format_simple_artist),
        'disc_number': result['disc_number'],
        'duration_ms': result['duration_ms'],
        'explicit': result['explicit'],
        'name': result['name'],
        'popularity': result['popularity'],
        'track_number': result['track_number'],
        'uri': result['uri'],
        'id': result['id'],
        'type': result['type']}
    
    return track
