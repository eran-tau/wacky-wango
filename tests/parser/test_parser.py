from wackywango.parsers import parsers
from wackywango.config import Config

config = Config()

user_id = 42
username = "Dan Gittik"
birthday = 699746400

sent_data = {}

host = '127.0.0.1'
port = '8000'


def test_loaded_parser():
    available_parsers = config.get_queue_keys()
    for parser in parsers.parser.parsers:
        assert parser.parser_type in available_parsers, "loaded a parser type that is not in the available list of config, you should add it "+parser.parser_type
        available_parsers.remove(parser.parser_type)
    assert len(available_parsers) == 0, "Missing parsers: " + repr(available_parsers)