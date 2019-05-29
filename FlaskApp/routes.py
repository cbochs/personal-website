import json
import urllib.parse

import requests

from flask import redirect, render_template, request, url_for
from FlaskApp import app
from FlaskApp.credentials import *
from FlaskApp.spotify_api import Spotify, SpotifyOAuth

scope = 'user-read-private playlist-read-private'


@app.route('/')
def index():
    title = 'Calvin Bochulak - Home'
    return render_template('index.html', title=title)


@app.route('/authorize', methods=['GET'])
def authorize():
    oauth = SpotifyOAuth(client_id, client_secret, redirect_uri)
    code = request.values.get('code')
    
    if code:
        token = oauth.request_access_token(code)
        sp = Spotify(token['access_token'])
        display_name = sp.me()['display_name']

        return redirect(url_for('user', display_name=display_name))
    else:
        url = oauth.get_authorization_url(scope)
        return redirect(url)


@app.route('/user')
def user():
    display_name = request.args.get('display_name')
    return render_template('user.html', display_name=display_name)