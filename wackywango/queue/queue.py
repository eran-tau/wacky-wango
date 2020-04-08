from .rabbitmq import RabbitMQDriver


class Queue:
    def __init__(self, url):
        self._driver = find_driver(url)

    def publish(self, exchange, routing_key, message):
        return self._driver.publish(exchange, routing_key, message)

    def consume(self, exchange, binding_key, callback):
        self._driver.consume(exchange, binding_key, callback)


def find_driver(url):
    for scheme, cls in drivers.items():
        if url.startswith(scheme):
            return cls(url)
    raise ValueError(f'invalid url: {url!r}')


drivers = {'rabbitmq://': RabbitMQDriver}
