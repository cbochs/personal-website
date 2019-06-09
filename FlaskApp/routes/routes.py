import json

from flask import redirect, render_template, request, url_for

from FlaskApp import app, mongo, oauth, scheduler
from FlaskApp.orm.create import create_user
from FlaskApp.orm.find import find_user, find_playlist
from FlaskApp.orm.jobs import schedule_recently_played, update_jobs
from FlaskApp.spotify.oauth import SpotifyOAuth

scope = ','.join(['playlist-read-private',
                  'playlist-read-collaborative',
                  'playlist-modify-public',
                  'playlist-modify-private',
                  'user-library-read',
                  'user-read-recently-played'])

logo = 'imsignificant!'


@app.route('/')
@app.route('/index')
def index():
    title = 'imsignificant! - Home'
    return render_template('index.html', title=title, logo=logo)


@app.route('/myspotify')
def myspotify():
    title = 'imsignificant! - MySpotify'
    return render_template('myspotify.html', title=title, logo=logo)


@app.route('/authorize', methods=['GET'])
def authorize():
    code = request.values.get('code')

    # temporary. use different oauth that is based on request's url for debugging
    if app.config.get('LOCAL_IP') in request.url_root:
        oauth_ = SpotifyOAuth(app, redirect_uri=app.config.get('LOCAL_REDIRECT'))
    else:
        oauth_ = oauth
    
    if code:
        token_info = oauth_.request_access_token(code)

        user = create_user(token_info)
        schedule_recently_played(user['user']['id'])

        return redirect(url_for('user', display_name=user['user']['id']))
    else:
        url = oauth_.get_authorization_url(scope)
        return redirect(url)


@app.route('/user')
def user():
    title = 'imsignificant! - MySpotify'
    display_name = request.args.get('display_name')
    return render_template('user.html', title=title, logo=display_name)


@app.route('/job')
@app.route('/job/<type_>/<id_>')
def job(type_=None, id_=None):
    title = 'imsignificant! - by Job!'

    if id_ is None:
        result = 'jobs updated'
        update_jobs()
    else:
        if type_ == 'user':
            result = f'RUN RECENTLY PLAYED FOR {id_}'
            scheduler.run_job(f'recently_played_{id_}')
        elif type_ == 'playlist':
            result = f'RUN JOB FOR PLAYLIST {id_}'
            scheduler.run_job(f'playlist_{id_}')
        else:
            result = 'NO JOB RUN'

    return render_template('job.html', title=title, logo=logo, result=result)


@app.route('/test')
def test():
    title = 'imsignificant! - Testo'
    result = 'Done!'
    return render_template('job.html', title=title, logo=logo, result=result)


@app.route('/update')
def users():
    for user in mongo.db.users.find({}):
        mongo.db.users.update_one(
            {'_id': user['_id']},
            {'$set': {'playlists': {'watching': []}}, '$rename': {'user_info': 'user'}})
    return redirect(url_for('index'))
