import pytest
from wackywango.server import server
from wackywango.queue import Queue

from wackywango.client import upload_sample

import time
from multiprocessing import Process
import json

user_id = 42
username = "Dan Gittik"
birthday = 699746400

sent_data = {}
cnt_feelings = 0

host = '127.0.0.1'
port1 = 8000
port2 = 8001


@pytest.fixture
def patched_requests(tmp_path, monkeypatch):

    def mocked_queue(uri, *args, **kwargs):
        p = tmp_path / "test2"
        w = open(p, "w")
        w.write(json.dumps({'username': args[1]}))
        w.close()
        return

    def mocked_init(uri, *args, **kwargs):
        # Do Nothing
        return

    monkeypatch.setattr(Queue, 'publish', mocked_queue)
    monkeypatch.setattr(Queue, '__init__', mocked_init)


def test_server_read_message(tmp_path):
    # Start the server
    def publish_test_method(path):
        def test_publish_wrapper(message):
            w = open(path, "w")
            w.write(json.dumps({'username': message.user.username}))
            w.close()
        return test_publish_wrapper
    p = tmp_path / "test"
    test_server = Process(target=server.run_server,
                          args=(host, port1, publish_test_method(p)))
    test_server.start()

    time.sleep(2)
    # Upload the sample
    upload_sample(host, port1, 'tests/small_sample.mind.gz')

    # Make sure the server got the message
    f = open(p, "r")
    data = json.loads(f.read())
    assert data['username'] == username

    test_server.terminate()
    test_server.join()
    time.sleep(2)



def test_server_message_queue(tmp_path, patched_requests):
    global cnt_feelings
    # Start the server
    test_server = Process(target=server.run_server_from_cli,
                          args=(host, port2, "rabbitmq://0.0.0.0:1234"))
    test_server.start()
    time.sleep(2)

    # Upload the sample
    upload_sample(host, port2, 'tests/small_sample.mind.gz')

    p = tmp_path / "test2"
    f = open(p, "r")
    data = json.loads(f.read())
    assert data['username'] == 'raw.feelings'

    # Make sure the server got the message
    test_server.terminate()
    test_server.join()
    time.sleep(2)
