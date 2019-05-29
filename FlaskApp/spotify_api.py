from time import time
from urllib.parse import urlencode

import requests


class SpotifyOAuthError(object):
    pass


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
            raise SpotifyOAuthError()

        token_info = response.json()
        token_info = self._add_expiry_time(token_info)

        return token_info


    def _add_expiry_time(self, token_info):
        token_info['expires_at'] = int(time()) + token_info['expires_in']
        return token_info
