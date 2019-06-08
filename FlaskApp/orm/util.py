from datetime import datetime

from app import mongo, oauth


def document_exists(collection, document):
    return collection.find({'id': document['id']}) \
                     .limit(1) \
                     .count(with_limit_and_skip=True) > 0


def is_token_expired(token_info):
    time = datetime.utcnow().timestamp()
    return (token_info['expires_at'] - time) < 60


def update_token_info(user):
    if is_token_expired(user['token_info']):
        token_info = oauth.refresh_access_token(user['token_info'])
    else:
        token_info = user['token_info']

    user['token_info'] = token_info
    mongo.db.users.update_one({'id': user['id']}, {'$set': user})

    return user


def chunks(list_, n):
    for i in range(0, len(list_), n):
        yield list_[i:i+n]