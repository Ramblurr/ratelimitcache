import sys
sys.path.insert(0, '..')
import random
from datetime import datetime

from flask import Flask, jsonify, request
from flaskext.cache import Cache

from ratelimitcache import ratelimit, ratelimit_post

app = Flask(__name__)
app.config.from_pyfile('hello.cfg')
cache = Cache(app)

@app.route('/api/minute')
@ratelimit(cache=cache.cache, minutes=1, requests=3)
def once_per_minute():
    return '%s <br /> <a href="/api/minute">refresh</a>' % (str(datetime.now()))

@app.route('/')
def root():
    return 'To test visit <a href="/api/minute">/api/minute</a>. You\'re allowed 3 requests per minute'

if __name__ == '__main__':
    app.run()
