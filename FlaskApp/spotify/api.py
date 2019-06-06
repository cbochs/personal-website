from time import time
from datetime import datetime, timedelta
from urllib.parse import urlencode

import requests
import os


class SpotifyException(BaseException):
    pass


class SpotifyOAuthException(BaseException):
    pass


class Spotify(object):

    API_URL = 'https://api.spotify.com/v1/'

    def __init__(self, access_token, token_type='Bearer'):
        self.access_token = access_token
        self.token_type = token_type

    
    def me(self, *args, **kwargs):
        return self._get('me', *args, **kwargs)

    
    def recently_played(self, *args, **kwargs):
        return self._get('me/player/recently-played', *args, **kwargs)

    
    def albums(self, *args, **kwargs):
        return self._get('albums', *args, **kwargs)

    
    def artists(self, *args, **kwargs):
        return self._get('artists', *args, **kwargs)

    
    def tracks(self, *args, **kwargs):
        return self._get('tracks', *args, **kwargs)


    def _get(self, endpoint, *args, **kwargs):
        url = os.path.join(self.API_URL, endpoint)
        headers = {'Authorization': f'{self.token_type} {self.access_token}'}
        
        response = requests.get(url, headers=headers, params=kwargs)

        if response.status_code != 200:
            print(response.json())
            raise SpotifyException()

        return response.json()


class SpotifyOAuth(object):

    OAUTH_AUTHORIZE_URL = 'https://accounts.spotify.com/authorize'
    OAUTH_TOKEN_URL = 'https://accounts.spotify.com/api/token'

    def __init__(self, client_id, client_secret, redirect_uri):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri


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
