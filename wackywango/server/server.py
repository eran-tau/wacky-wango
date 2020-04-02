from flask import Flask
from flask import request
from flask import current_app
from ..proto import cortex_pb2
from ..queue import Queue
import uuid

queue_keys = ['pose','color_image','depth_image','feelings']
#Todo: Move to config
# supported_formats={'pose':'pose','depth_image':'depth-image','feelings':'feelings'}


def run_server_from_cli(host,port,url):
    def my_publish(message):
        queue = Queue(url)
        unique_filename = "raw_data/" + str(uuid.uuid4())
        newFile = open(unique_filename, "wb")
        newFile.write(message.SerializeToString())
        for key in queue_keys:
            if message.snapshot.HasField(key):
                queue.publish('exchange','raw.'+key, {"data":unique_filename,"parser_type":key})
    run_server(host,port,my_publish)

def run_server(host,port,publish):
    app.config['publish'] = publish
    app.run(host, port)

app = Flask(__name__)

@app.route('/snapshot', methods=['POST'])
def snapshot():
    upload_snapshot = cortex_pb2.UploadSnapshot()
    upload_snapshot.ParseFromString(request.data)
    current_app.config['publish'](upload_snapshot)
    return 'OK'


