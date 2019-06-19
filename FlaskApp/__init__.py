from flask import Flask
from flask_apscheduler import APScheduler
from flask_cors import CORS
from flask_pymongo import PyMongo
from FlaskApp.jsonencoder import JSONEncoder
from FlaskApp.spotify.oauth import SpotifyOAuth

app = Flask(__name__)
app.config.from_envvar('FLASK_CFG')
app.json_encoder = JSONEncoder

CORS(app)

mongo = PyMongo(app)

scheduler = APScheduler(app=app)
scheduler.start()

oauth = SpotifyOAuth(app)

from FlaskApp import routes
