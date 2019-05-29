import json

from flask import redirect, render_template, request, url_for
from FlaskApp import app
from FlaskApp.credentials import (CLIENT_ID, CLIENT_SECRET, LOCAL_IP,
                                  LOCAL_REDIRECT, REDIRECT_URI)
from FlaskApp.jsonencoder import JSONEncoder
from FlaskApp.mongo import find_user, setup_user
from FlaskApp.spotify_api import SpotifyOAuth

scope = 'playlist-read-private playlist-read-collaborative'


@app.route('/')
def index():
    title = 'Calvin Bochulak - Home'
    return render_template('index.html', title=title)


@app.route('/authorize', methods=['GET'])
def authorize():
    redirect_uri = REDIRECT_URI if LOCAL_IP not in request.base_url else LOCAL_REDIRECT
    oauth = SpotifyOAuth(CLIENT_ID, CLIENT_SECRET, redirect_uri)
    code = request.values.get('code')
    
    if code:
        token_info = oauth.request_access_token(code)
        user = setup_user(token_info)

        return redirect(url_for('user', display_name=user['user_id']))
    else:
        url = oauth.get_authorization_url(scope)
        return redirect(url)


@app.route('/access_token')
def access_token():
    user_id = request.values.get('user_id')
    user = find_user(user_id)
    return json.dumps(user, cls=JSONEncoder), 200


@app.route('/user')
def user():
    display_name = request.args.get('display_name')
    return render_template('user.html', display_name=display_name)
