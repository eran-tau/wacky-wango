from flask import Flask
from flask import request
import uuid
from ..proto import cortex_pb2
import pika


def run_server(host,port,publish):
    server.start(host,port,publish)


class Server:
    def start(self, host, port, publish):
        app.run(host, port)


server = Server()
app = Flask(__name__)

@app.route('/config', methods=['GET'])
def config():
    return "TODO"


@app.route('/snapshot', methods=['POST'])
def snapshot():
    upload_snapshot = cortex_pb2.UploadSnapshot()
    upload_snapshot.ParseFromString(request.data)
    params = pika.ConnectionParameters('localhost')
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue='hello')
    channel.basic_publish(
        exchange='',
        routing_key='hello',
        body=upload_snapshot.SerializeToString(),
    )

    return 'Hello, World!'


