# from time import sleep
#
# import requests
# import redis
#
# r = redis.Redis(host='redis', port=6379)
#
#
# def update_status():
#     sleep(1)
#     while True:
#         for service in ['localhost:9081', 'localhost:9082']:
#             try:
#                 response = requests.get(f"http://{service}/healthcheck", timeout=1)
#                 if response.ok:
#                     if r.get(service) > 0:
#                         r.decr(service)
#                         print(f"{service} {r.get('service')}", flush=True)
#                     else:
#                         r.set(service, 0)
#                         r.set('service', service)
#                         print(f"{service} {r.get('service')}", flush=True)
#                 else:
#                     r.delete(service)
#                     print(f"{service} dead", flush=True)
#             except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
#                 r.delete(service)
#                 print(f"{service} is 100% dead", flush=True)
#         sleep(5)
