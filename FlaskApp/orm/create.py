from FlaskApp import mongo, scheduler
from FlaskApp.orm.fetch import fetch_user
from FlaskApp.orm.util import document_exists
from FlaskApp.orm.update import update_recently_played
from pymongo.errors import DuplicateKeyError


def create_user(token_info):
    user_info = fetch_user(token_info)

    user = {
        'user_info': user_info,
        'token_info': token_info,
        'recently_played': {
            'active': True,
            'last_checked': None}}
    
    user_id = user['user_info']['id']

    if not document_exists(mongo.db.users, {'user_info.id': user_id}):       
        try:
            mongo.db.users.insert_one(user)

            scheduler.add_job(
                f'recently_played_{user_id}',
                update_recently_played, args=[user_id],
                trigger='cron', minute=0, hour='*/2')
        except DuplicateKeyError as e:
            print('ATTEMPTED TO INSERT DUPLICATE USER')
    
    return user

