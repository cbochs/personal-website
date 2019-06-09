import json

from flask import redirect, render_template, request, url_for
from FlaskApp import app, oauth, scheduler
from FlaskApp.orm.create import create_user
from FlaskApp.orm.find import find_user
from FlaskApp.orm.update import update_jobs
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

        return redirect(url_for('user', display_name=user['user_info']['id']))
    else:
        url = oauth_.get_authorization_url(scope)
        return redirect(url)


@app.route('/user')
def user():
    title = 'imsignificant! - MySpotify'
    display_name = request.args.get('display_name')
    return render_template('user.html', title=title, logo=display_name)


@app.route('/job')
@app.route('/job/<user_id>')
def job(user_id=None):
    title = 'imsignificant! - by Job!'

    if user_id is None:
        result = 'jobs updated'
        update_jobs()
    else:
        result = f'run job for {user_id}'
        scheduler.run_job(f'recently_played_{user_id}')

    return render_template('job.html', title=title, logo=logo, result=result)
