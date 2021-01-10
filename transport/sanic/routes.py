from transport.sanic.endpoints.health import health_endpoint


def get_routes():
    return (
        (health_endpoint, '/', ['POST', 'GET']),
    )