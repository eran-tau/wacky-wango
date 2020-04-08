from ..queue import Queue
import json
import pathlib
from .parser_helper import Parser

parser = Parser()
parser.load_parsers(pathlib.Path(__file__).parent.absolute() / "my_parsers")


def parse(parser_type, data):
    return json.dumps(parser.parse(parser_type, data))


def run_parser(parser_type, url):
    def callback(channel, method, properties, body):
        print(f'consumed {body}')
        queue_data = json.loads(body)
        results = parser.parse(queue_data['parser_type'], queue_data['data'])
        for result in results:
            queue.publish('exchange', 'parsed.'+queue_data['parser_type'],
                          result)

    queue = Queue(url)
    queue.consume('exchange', 'raw.'+parser_type, callback)
