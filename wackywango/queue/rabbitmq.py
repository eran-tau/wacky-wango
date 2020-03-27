import pika

class RabbitMQDriver:

    def __init__(self, url):
        proper_url = 'amqp' + url[8:]
        params = pika.URLParameters(proper_url)
        connection = pika.BlockingConnection(params)
        self.channel = connection.channel()
        #TODO: Consider changing to a constant?
        self.channel.queue_declare(queue='wackywango')


    def publish(self, key, message):
        return self.channel.basic_publish(
            exchange='',
            routing_key=key,
            body=message,
        )


