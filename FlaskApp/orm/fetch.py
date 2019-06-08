from FlaskApp.formatter import *
from FlaskApp.spotify.api import Spotify
from FlaskApp.orm.find import find_user
from FlaskApp.orm.util import update_token_info


# TODO fetch_saved_tracks
#      - create fetch function
#      - create formatting function for saved_tracks
#      - store saved tracks in user or as playlist?


def fetch_user(token_info):
    token_info = update_token_info(token_info)
    sp = Spotify(token_info)
    return format_user(sp.me())


def fetch_recently_played(user_id):
    user = find_user(user_id)
    sp = Spotify(user['token_info'])

    return format_all(sp.recently_played(no_cursor=True),
                      format_play_history, user=user['user_info'])


def fetch_albums(album_ids):
    user = find_user('notbobbobby')
    sp = Spotify(user['token_info'])

    return format_all(sp.albums(ids=album_ids), format_album)


def fetch_artists(artist_ids):
    user = find_user('notbobbobby')
    sp = Spotify(user['token_info'])

    return format_all(sp.artists(ids=artist_ids), format_artist)


def fetch_tracks(track_ids, limit=50):
    user = find_user('notbobbobby')
    sp = Spotify(user['token_info'])

    return format_all(sp.tracks(ids=track_ids), format_track)


def fetch_playlist(playlist_id):
    user = find_user('notbobbobby')
    sp = Spotify(user['token_info'])

    return format_playlist(sp.playlist(playlist_id, no_cursor=True))
