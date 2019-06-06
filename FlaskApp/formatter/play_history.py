from FlaskApp.formatter.datetime import to_datetime
from FlaskApp.formatter.track import format_simple_track


def format_play_history(result, user):
    play_history = {
        'context': result['context'],
        'played_at': to_datetime(result['played_at'], 'ms'),
        'track': format_simple_track(result['track']),
        'user': user,
        'type': 'play_history'}
    
    return play_history
