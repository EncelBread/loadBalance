from loadbalancer import loadbalancer


def test_requests(client):
    while True:
        client.get('/')


client = loadbalancer.test_client()
test_requests(client)
