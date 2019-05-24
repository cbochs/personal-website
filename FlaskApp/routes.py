from flask import render_template
from FlaskApp import app

@app.route('/')
@app.route('/index')
def hello():
    user = {'username': 'Calvin Cool'}
    posts = [
        {'author': {'username': 'John'}, 'body': 'Beautiful day in Portland!'},
        {'author': {'username': 'Susan'}, 'body': 'The Avengers movie was so cool!'}
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)