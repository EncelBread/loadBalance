from flask import Flask
import requests
import time

import redis

# counting active connections number by server in Redis
r = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

loadbalancer = Flask(__name__)

# TODO config
BACKENDS = ['localhost:9081', 'localhost:9082', 'localhost:9083', 'localhost:9084', 'localhost:9085']


@loadbalancer.route('/')
@loadbalancer.route("/test")
def router():
    service = r.get('service')
    r.incr(service)
    time.sleep(1)  # testing balancer
    response = requests.get(f'http://{service}')
    r.decr(service)
    n = float('inf')
    next_service = None
    for key in r.keys():
        if key != 'service':
            if float(r.get(key)) < n:
                n = float(r.get(key))
                next_service = key
    if n != float('inf'):
        r.set('service', next_service)
    return response.content, response.status_code
