from .rabbitmq import RabbitMQDriver

class Queue:
    def __init__(self, url):
        self._driver = find_driver(url)
    def publish(self, key, message):
        id = self._driver.publish(key,message)
        return id

def find_driver(url):
    for scheme, cls in drivers.items():
        if url.startswith(scheme):
            return cls(url)
    raise ValueError(f'invalid url: {url!r}')

drivers = {'rabbitmq://': RabbitMQDriver}
