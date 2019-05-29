import json
import urllib.parse

import requests

from flask import redirect, render_template, request
from FlaskApp import app
from FlaskApp.credentials import *
from FlaskApp.spotify_api import SpotifyOAuth

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
        return json.dumps(token)
    else:
        url = oauth.get_authorization_url(scope)
        return redirect(url)
