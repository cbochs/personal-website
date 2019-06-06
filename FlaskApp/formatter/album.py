from FlaskApp.formatter.artist import format_simple_artist
from FlaskApp.formatter.util import format_all
from FlaskApp.formatter.datetime import to_datetime

def format_simple_album(result):
    album = {
        'artists': format_all(result['artists'], format_simple_artist),
        'name': result['name'],
        'id': result['id'],
        'type': result['type']}

    return album


def format_album(result):
    album = {
        'album_type': result['album_type'],
        'artists': format_all(result['artists'], format_simple_artist),
        'copyrights': result['copyrights'],
        'genres': result['genres'],
        'name': result['name'],
        'popularity': result['popularity'],
        'release_date': to_datetime(result['release_date'],
                                    result['release_date_precision']),
        'release_date_precision': result['release_date_precision'],
        'total_tracks': result['total_tracks'],
        'uri': result['uri'],
        'id': result['id'],
        'type': result['type']}

    return album