from flask import Flask
from flask import request
from flask import current_app
from ..proto import cortex_pb2
from ..queue import Queue
from ..config import Config
import uuid

config = Config()
app = Flask(__name__)


def run_server_from_cli(host,port,url):
    def my_publish(message):
        queue = Queue(url)
        unique_filename = config.data['path']+"/raw_data/" + str(uuid.uuid4())
        newFile = open(unique_filename, "wb")
        newFile.write(message.SerializeToString())
        for key in config.get_queue_keys():
            if message.snapshot.HasField(key) and  getattr(message.snapshot, key).ByteSize() > 0 :
                queue.publish('exchange','raw.'+key, {"data":unique_filename,"parser_type":key})
    run_server(host,port,my_publish)

def run_server(host,port,publish):
    app.config['publish'] = publish
    app.run(host, port)


@app.route('/snapshot', methods=['POST'])
def snapshot():
    upload_snapshot = cortex_pb2.UploadSnapshot()
    upload_snapshot.ParseFromString(request.data)
    current_app.config['publish'](upload_snapshot)
    return 'OK'


