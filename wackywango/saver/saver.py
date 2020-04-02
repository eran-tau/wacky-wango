from ..proto import cortex_pb2
from ..database import Database
from ..queue import Queue
import json

class Saver:
    def __init__(self, database_url):
        self.db = database_url


def save_once():
    return 1

def run_saver(database_url, queue_url):
    def callback(channel, method, properties, body):
        data = json.loads(body)
        save_result(data,database_url)

    url = queue_url
    queue = Queue(url)
    queue.consume('exchange','parsed.*',callback)


def save_result(result,database_url):
    url = database_url
    database = Database(url)
    user = database.get_user(result['user_data']['userId'])
    if not user:
        database.create_user(result['user_data']['userId'],result['user_data']['username'],result['user_data']['birthday'])

    database.add_snapshot(result['snapshot_timestamp'],result['parser_type'],result['snapshot_data'])





