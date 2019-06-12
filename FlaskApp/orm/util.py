from datetime import datetime

from FlaskApp import mongo, oauth


def document_exists(collection, query):
    return collection.find(query) \
                     .limit(1) \
                     .count(with_limit_and_skip=True) > 0


def is_token_expired(token_info):
    time = datetime.utcnow().timestamp()
    return (token_info['expires_at'] - time) < 300


def update_token_info(token_info):
    if is_token_expired(token_info):
        token_info = oauth.refresh_access_token(token_info)
    return token_info


def update_user(user):
    user['token_info'] = update_token_info(user['token_info'])
    mongo.db.users.update_one(
        {'user.id': user['user']['id']},
        {'$set': {'token_info': user['token_info']}})

    return user
