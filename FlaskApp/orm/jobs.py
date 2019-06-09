from FlaskApp import mongo, scheduler
from FlaskApp.orm.update import update_recently_played, update_playlist


def update_jobs():
    # temporary fix because when the server restarts idk what to do...
    mongo.db.jobs.remove({})

    for user in mongo.db.users.find({}):
        user_id = user['user']['id']
        
        if user['recently_played']['active']:
            schedule_recently_played(user_id)
        
        for playlist_id in user['playlists']['watching']:
            schedule_playlist(playlist_id)


def schedule_recently_played(user_id):
    if not scheduler.get_job(f'recently_played_{user_id}'):
        scheduler.add_job(
            f'recently_played_{user_id}',
            update_recently_played, args=[user_id],
            trigger='cron', minute=0, hour='*/2')


def schedule_playlist(playlist_id):
    if not scheduler.get_job(f'playlist_{playlist_id}'):
        scheduler.add_job(
            f'playlist_{playlist_id}',
            update_playlist, args=[playlist_id],
            trigger='cron', hour='*/6')