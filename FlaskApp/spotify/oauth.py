from datetime import datetime, timedelta
from time import time
from urllib.parse import urlencode

import requests


class SpotifyOAuthException(BaseException):
    pass


class SpotifyOAuth(object):

    OAUTH_AUTHORIZE_URL = 'https://accounts.spotify.com/authorize'
    OAUTH_TOKEN_URL = 'https://accounts.spotify.com/api/token'

    def __init__(self, app=None, client_id=None, client_secret=None, redirect_uri=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

        if app is not None:
            self.init_app(app, client_id, client_secret, redirect_uri)


    def init_app(self, app, client_id=None, client_secret=None, redirect_uri=None):

        if client_id is None:
            self.client_id = app.config.get('CLIENT_ID', None)
        
        if client_secret is None:
            self.client_secret = app.config.get('CLIENT_SECRET', None)
        
        if redirect_uri is None:
            self.redirect_uri = app.config.get('REDIRECT_URI', None)


    def get_authorization_url(self, scope=''):
        params = {
            'client_id': self.client_id,
            'response_type': 'code',
            'redirect_uri': self.redirect_uri,
            'scope': scope}

        return self.OAUTH_AUTHORIZE_URL + '?' + urlencode(params)

    
    def request_access_token(self, code):
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self.redirect_uri}
        # headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        response = requests.post(self.OAUTH_TOKEN_URL, data=data)

        if response.status_code != 200:
            raise SpotifyOAuthException()

        token_info = response.json()
        token_info = self._add_expiry_time(token_info)

        return token_info

    
    def refresh_access_token(self, token_info):
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'refresh_token',
            'refresh_token': token_info['refresh_token']}
        # headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        response = requests.post(self.OAUTH_TOKEN_URL, data=data)

        if response.status_code != 200:
            raise SpotifyOAuthException()

        # keep old token in case no new token provided
        refresh_token = token_info['refresh_token']

        token_info = response.json()
        token_info = self._add_expiry_time(token_info)

        if 'refresh_token' not in token_info:
            token_info['refresh_token'] = refresh_token
        
        return token_info


    def _add_expiry_time(self, token_info):
        dt = datetime.utcnow() + timedelta(seconds=token_info['expires_in'])
        token_info['expires_dt'] = dt
        token_info['expires_at'] = int(dt.timestamp())
        return token_info
