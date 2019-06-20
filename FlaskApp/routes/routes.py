import json

from flask import jsonify, redirect, render_template, request, url_for

from FlaskApp import app, mongo, oauth, scheduler
from FlaskApp.orm.create import create_user
from FlaskApp.orm.find import find_playlist, find_recently_played, find_user
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
        user_id = user['user']['id']

        schedule_recently_played(user_id)

        return redirect(url_for('user', user_id=user_id))
    else:
        url = oauth_.get_authorization_url(scope)
        return redirect(url)


@app.route('/user')
@app.route('/user/<user_id>')
def user(user_id):
    title = 'imsignificant! - MySpotify'
    return render_template('user.html', title=title, logo=user_id)


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


@app.route('/history', methods=['POST'])
def recently_played():
    data = request.get_json()
    return jsonify(find_recently_played(**data))
