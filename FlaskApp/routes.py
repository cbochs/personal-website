from flask import redirect, render_template, request, url_for
from FlaskApp import app
from FlaskApp.credentials import *
from FlaskApp.spotify_api import SpotifyOAuth
from FlaskApp.mongo import setup_user, find_user

import json
from FlaskApp.jsonencoder import JSONEncoder

scope = 'user-read-private playlist-read-private playlist-read-collaborative'


@app.route('/')
def index():
    title = 'Calvin Bochulak - Home'
    return render_template('index.html', title=title)


@app.route('/authorize', methods=['GET'])
def authorize():
    oauth = SpotifyOAuth(client_id, client_secret, redirect_uri)
    code = request.values.get('code')
    
    if code:
        token_info = oauth.request_access_token(code)
        user = setup_user(token_info)

        return redirect(url_for('user', display_name=user['display_name']))
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