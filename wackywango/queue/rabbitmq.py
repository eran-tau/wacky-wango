import pika
import json

class RabbitMQDriver:

    def __init__(self, url):
        proper_url = 'amqp' + url[8:]
        params = pika.URLParameters(proper_url)
        connection = pika.BlockingConnection(params)
        self.channel = connection.channel()

    def publish(self, exchange, routing_key, message):
        self.channel.exchange_declare(exchange=exchange, exchange_type='topic')
        print(f'About to publish {message}')
        return self.channel.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=json.dumps(message)
        )

    def consume(self,exchange, binding_key,callback):
        self.channel.exchange_declare(exchange=exchange, exchange_type='topic')
        result = self.channel.queue_declare('', exclusive=True)
        queue_name = result.method.queue
        self.channel.queue_bind(
            exchange=exchange, queue=queue_name, routing_key=binding_key)

        self.channel.basic_consume(
            queue=queue_name,
            on_message_callback=callback,
            auto_ack=True
        )

        self.channel.start_consuming()


