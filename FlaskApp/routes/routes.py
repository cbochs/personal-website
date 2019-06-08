import json

from flask import redirect, render_template, request, url_for
from FlaskApp import app, oauth

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
    
    if code:
        token_info = oauth.request_access_token(code)
        user = create_user(token_info)

        return redirect(url_for('user', display_name=user['id']))
    else:
        url = oauth.get_authorization_url(scope)
        return redirect(url)


@app.route('/user')
def user():
    title = 'imsignificant! - MySpotify'
    display_name = request.args.get('display_name')
    return render_template('user.html', title=title, logo=display_name)


@app.route('/test')
def test():
    title = 'imsignificant! - Test'
    return render_template('test.html', title=title, logo=logo, items='no')