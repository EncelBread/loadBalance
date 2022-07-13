from flask import Flask
import requests
import yaml
import time

import redis

# Храним количество активных подключений у серверов в оперативной памяти (Redis) + 'service' - следующий сервер
r = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

loadbalancer = Flask(__name__)

# TODO вынести в конфиг
BACKENDS = ['localhost:9081', 'localhost:9082', 'localhost:9083', 'localhost:9084', 'localhost:9085']


@loadbalancer.route('/')
@loadbalancer.route("/test")
def router():
    service = r.get('service')
    # замена обработчика входящих запросов (4/7 уровень)
    r.incr(service)
    time.sleep(1)  # для тестирования балансировщика
    response = requests.get(f'http://{service}')
    r.decr(service)
    # Обработка идёт по запросу, а не timeout - в идеале вынести в healthcheck
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
