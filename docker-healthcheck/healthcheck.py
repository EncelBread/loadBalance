from time import sleep

import requests
import redis

r = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

is_active = False  # flag: is there any active server?
servers = ['localhost:9081', 'localhost:9082', 'localhost:9083', 'localhost:9084', 'localhost:9085']


def check_services(is_active, servers):
    for service in servers:
        try:
            response = requests.get(f"http://{service}/healthcheck", timeout=1)
            if response.ok:
                r.set('service', service)
                if not is_active:
                    r.set(service, 0)
                    is_active = True
            else:
                print(f"{service} dead", flush=True)
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            print(f"{service} is 100% dead", flush=True)


check_services(False, servers)

while True:
    for service in servers:
        try:
            response = requests.get(f"http://{service}/healthcheck", timeout=1)
            if response.ok:
                if not r.get(service):
                    r.set(service, 0)
                    r.set('service', service)
                elif r.get(service) == 0:
                    r.set('service', service)
                print(f"{service} {r.get(service)}", flush=True)
            else:
                r.delete(service)
                print(f"{service} dead", flush=True)
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            r.delete(service)
            print(f"{service} is 100% dead", flush=True)
    sleep(10)
