import json
import urllib.parse

import requests

from credentials import client_id, client_secret, redirect_uri
from flask import redirect, render_template, request
from FlaskApp import app


scope = ''


@app.route('/')
def index():
    title = 'Calvin Bochulak - Home'
    return render_template('index.html', title=title)


@app.route('/authorize', methods=['GET'])
def authorize():
    authorize_endpoint = 'https://accounts.spotify.com/authorize'
    params = {
        'client_id': client_id,
        'response_type': 'code',
        'redirect_uri': redirect_uri,
        'show_dialog': True}
    
    code = request.values.get('code')
    if code:
        return redirect('/')
    else:
        return redirect(authorize_endpoint + '?' + urllib.parse.urlencode(params))
