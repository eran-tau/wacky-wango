from flask import Flask
from flask import request
from flask import current_app
from ..proto import cortex_pb2
from ..queue import Queue

supported_formats={'pose':'pose','color_image':'color-image','depth_image':'depth-image','feelings':'feelings'}

def run_server_from_cli(host,port,url):
    def my_publish(message):
        queue = Queue(url)
        for key  in supported_formats:
            if message.snapshot.HasField(key):
                print("publishing"+key)
                queue.publish(supported_formats[key], message.SerializeToString())

    run_server(host,port,my_publish)

def run_server(host,port,publish):
    server = Server(publish)
    app.config['server'] = server
    app.run(host, port)


class Server:
    def __init__(self,publish):
        self.publish = publish

    def publish_message(self, message):
        self.publish(message)


app = Flask(__name__)

@app.route('/config', methods=['GET'])
def config():
    return "TODO"


@app.route('/snapshot', methods=['POST'])
def snapshot():
    upload_snapshot = cortex_pb2.UploadSnapshot()
    upload_snapshot.ParseFromString(request.data)
    current_app.config['server'].publish_message(upload_snapshot)
    return 'Hello, World!'


