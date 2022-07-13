import threading
from flask import Flask
import time, traceback
import requests
import redis

r = redis.Redis(host='redis', port=6379)


app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return str(sum([pow(78,34) for num in range(10000000)]))


@app.route('/healthcheck')
def healthcheck():
    return "OK"


if __name__ == '__main__':
    app.run(host='0.0.0.0')
