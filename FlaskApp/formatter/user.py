

def format_basic_user(result):
    user = {
        'id': result['id'],
        'type': result['type']}

    return user


def format_simple_user(result):
    user = {
        'display_name': result['display_name'],
        'id': result['id'],
        'type': result['type']}

    return user


def format_user(result, token_info):
    user = {
        'display_name': result['display_name'],
        'followers': result['followers']['total'],
        'uri': result['uri'],
        'token_info': token_info,
        'id': result['id'],
        'type': result['type']}

    return user