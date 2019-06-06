from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config.from_envvar('FLASK_CFG')

mongo = PyMongo(app)

from FlaskApp.spotify.api import SpotifyOAuth
from FlaskApp.credentials import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
oauth = SpotifyOAuth(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)


from FlaskApp.jsonencoder import JSONEncoder
app.json_encoder = JSONEncoder


from FlaskApp import routes
