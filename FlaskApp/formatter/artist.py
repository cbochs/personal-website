

def format_simple_artist(result):
    artist = {
        'name': result['name'],
        'id': result['id'],
        'type': result['type']}

    return artist


def format_artist(result):
    artist = {
        'followers': result['followers']['total'],
        'genres': result['genres'],
        'name': result['name'],
        'popularity': result['popularity'],
        'id': result['id'],
        'type': result['type']}

    return artist