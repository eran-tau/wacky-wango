import pytest
import requests
from wackywango.proto import cortex_pb2
from wackywango.client import upload_sample

from urllib.parse import urlparse

user_id = 42
username = "Dan Gittik"
birthday = 699746400

sent_data = {}

host = '127.0.0.1'
port = '8000'

@pytest.fixture
def patched_requests(monkeypatch):
    # store a reference to the old get method
    def mocked_post(uri, *args, **kwargs):
        global sent_data
        parsed_uri = urlparse(uri)

        sent_data['endpoint'] = parsed_uri.path
        sent_data['host'] = parsed_uri.netloc.split(":")[0]
        sent_data['port'] = parsed_uri.netloc.split(":")[1]
        sent_data['data'] = kwargs['data']
        return

    # patch requests.post with patched version
    monkeypatch.setattr(requests, 'post', mocked_post)


def test_correct_endpoint(patched_requests):
    upload_sample(host, port, 'tests/small_sample.mind.gz')
    # upload_snapshot = cortex_pb2.UploadSnapshot()
    assert sent_data['endpoint'] == '/snapshot'
    assert sent_data['host'] == host
    assert sent_data['port'] == port


def test_user_attributes(patched_requests):
    upload_sample(host, port, 'tests/small_sample.mind.gz')
    upload_snapshot = cortex_pb2.UploadSnapshot()
    upload_snapshot.ParseFromString(sent_data['data'])
    assert upload_snapshot.user.user_id == user_id
    assert upload_snapshot.user.username == username
    assert upload_snapshot.user.birthday == birthday

