import json

from flask import redirect, render_template, request, url_for
from FlaskApp import app, oauth
from FlaskApp.jsonencoder import JSONEncoder
from FlaskApp.mongo import find_user, setup_user

scope = ','.join(['playlist-read-private',
                  'playlist-read-collaborative',
                  'playlist-modify-public',
                  'playlist-modify-private',
                  'user-library-read',
                  'user-read-recently-played'])
logo = 'imsignificant!'


@app.route('/')
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
    title = 'imsignificant! - MySpotify'
    display_name = request.args.get('display_name')
    return render_template('user.html', title=title, logo=display_name)
