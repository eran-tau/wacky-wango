from ..proto import cortex_pb2
from ..database import Database
from ..queue import Queue
import json


def save_once(database_url,parser_type,data):
    input = open(data, "r").read()
    input = json.loads(input)
    return save_result(parser_type,input[0], database_url)


def run_saver(database_url, queue_url):
    def callback(channel, method, properties, body):
        data = json.loads(body)
        save_result(data['parser_type'], data, database_url)

    url = queue_url
    queue = Queue(url)
    queue.consume('exchange', 'parsed.*', callback)


def save_result(parser_type,result,database_url):
    url = database_url
    database = Database(url)
    user = database.get_user(result['user_data']['userId'])
    if not user:
        database.create_user(result['user_data']['userId'],result['user_data']['username'],result['user_data']['birthday'])

    database.add_snapshot(result['user_data']['userId'],result['snapshot_timestamp'],parser_type,result['snapshot_data'])





